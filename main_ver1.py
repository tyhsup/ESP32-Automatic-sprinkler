from machine import ADC,Pin
from umqtt.robust import MQTTClient
import time,dht,BlynkLib,_thread,gc,machine,statistics
from BlynkTimer import BlynkTimer

#thingspeak 設定
mq_server = 'mqtt3.thingspeak.com'#thingspeak 伺服器
mq_id = 'ExIUCCk8JgIsKjgaLzI5LRU' #thingspeak格式ID
mq_topic= 'channels/' + '2032111' + '/publish'#thingspeak 伺服器topic格式
mq_user = 'ExIUCCk8JgIsKjgaLzI5LRU'  #thingspeak格式帳號
mq_pass = 'AgB2iyveE2Si2hcRdX8l7Jxe' #thingspeak格式密碼
mqClient0 = MQTTClient(mq_id,mq_server,user=mq_user,password=mq_pass,keepalive=60)
mqClient0.connect(False)


#Blynk設定
token ='lK8Kqo7Wqn30oQlInMfmashfv6YMamqR'# Blynk 權杖
blynk = BlynkLib.Blynk(token)            # 取得 Blynk 物件


#感測器及腳位設定
soil_Moisture=ADC(Pin(39))
soil_Moisture.atten(ADC.ATTN_11DB)
soil_Moisture.width(ADC.WIDTH_12BIT)
dht_power=Pin(36,Pin.OUT)
water_Level=ADC(Pin(36))
water_Level.atten(ADC.ATTN_11DB)
water_Level.width(ADC.WIDTH_12BIT)
water_valve=Pin(33,Pin.OUT)
d22=dht.DHT22(Pin(34)) 
EMI_Pin=ADC(Pin(35))
EMI_Pin.atten(ADC.ATTN_11DB)
EMI_Pin.width(ADC.WIDTH_12BIT)
BASE_Pin=Pin(22,Pin.OUT)
#線程鎖設定
lock=_thread.allocate_lock()


try:
    def wifi_connect_check():
        if wifi.isconnected():
            blynk.virtual_write(9, 'wifi connected')
        else:
            wifi.connect('ASUS_20_2G','sum998888')
            blynk.virtual_write(9, 'retry connect wifi')


    def soil_moisture_cal():		#計算土壤濕度
        gc.collect()				#reset 記憶體
        soil_moisture_list=[]
        i=0
        for i in range(400):#設定取樣範圍
            soil_moisture_val=(((soil_Moisture.read()/4095*3.3)*100-210)/0.65)#將電壓轉換為乾度%, over:3.3V,全濕:2.1V, 空氣約2.75v
            soil_moisture_list.append(soil_moisture_val)
            time.sleep(0.01)
        soil_moisture_medi=statistics.median(soil_moisture_list)#計算中位數
        return soil_moisture_medi


    def water_Level_cal():
        water_Level_val=(water_Level.read()/4095*3.3)#讀取water level sensor電壓值
        return water_Level_val

    def EMI_Pin_val_cal():
        EMI_Pin_val=(EMI_Pin.read()/4095*3.3)
        return EMI_Pin_val
    
    def v0_handler(value):             # 從 V0 虛擬腳位讀取手機按鈕狀態的函式
            value(int(value[0]))
            if reset_OC == 0:
                pass
            else:
                machine.reset()
    blynk.on("V0", v0_handler)     # 註冊由 v0_handler 處理 V0 虛擬腳位

    def d22_handler():            # 回應 Blynk 讀取 V1/V3 虛擬腳位的函式
        gc.collect()
        dht_power.init()
        dht_power.value(True)
        time.sleep(2)
        d22.measure()                # DHT22開始量測 
        blynk.virtual_write(1, d22.temperature()) #讀取溫度
        blynk.virtual_write(3, d22.humidity()) #讀取溼度
        dht_power.value(False)

    def v2_handler():				# 提供soil moisture電壓到V2的函式
        blynk.virtual_write(2, '{}'.format(soil_moisture_cal()))

    def v4_handler(value):             # 從 V4 虛擬腳位讀取手機按鈕狀態的函式
        BASE_Pin.value(int(value[0]))
    blynk.on("V4",v4_handler)          # 註冊由 v4_handler 處理 V4 虛擬腳位

    def v5_handler():             # 提供water level sensor電壓到V2的函式
        blynk.virtual_write(5, '{}'.format(water_Level_cal()))


    def LED_handler():				# 定義土壤乾燥指示燈的函式
        if soil_moisture_cal()>50:
            blynk.virtual_write(6,255)
            blynk.virtual_write(7,0)
        else:
            blynk.virtual_write(6,0)
            blynk.virtual_write(7,255)

        
    def thingspeak_update():
        while True:
            if EMI_Pin_val_cal()>1:
                mq_message='field1=' + '{}'.format(soil_moisture_cal()) + '&field2=' + '{}'.format(d22.temperature()) + '&field3=' + '{}'.format(d22.humidity()) 
                #上面這行是thingspeak表格格式+感測器讀值
                mqClient0.publish(mq_topic,mq_message)
            time.sleep(20)

    def water_valve_OC_controller():
        if soil_moisture_cal()>50:
            if water_Level_cal()==0:
                water_valve.value(1)
            else:
                water_valve.value(0)
        else:
            water_valve.value(0)

        
    _thread.start_new_thread(thingspeak_update,())

    timer = BlynkTimer()               # 建立計時器管理物件
    timer.set_interval(10, d22_handler)  # 建立每10秒觸發的計時器
    timer.set_interval(10, v2_handler)  # 建立每10秒觸發的計時器
    timer.set_interval(10, v5_handler)  # 建立每10秒觸發的計時器
    timer.set_interval(10, LED_handler)  # 建立每10秒觸發的計時器
    timer.set_interval(10, wifi_connect_check)# 建立每10秒觸發的計時器

    while True:
        blynk.run()                       # 持續檢查是否有收到 Blynk 送來的指令
        timer.run()                       # 持續檢查是否觸發計時器
        water_valve_OC_controller()
        if blynk.connected == False:
            machine.reset()
        else:
            pass

except Exception as e:
        blynk.log_event("error_code",str(e))
        machine.reset()
        
