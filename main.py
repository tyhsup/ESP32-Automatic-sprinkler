from machine import ADC,Pin
from umqtt.robust import MQTTClient
from BlynkTimer import BlynkTimer
import time,dht,BlynkLib,machine,statistics,gc
import ESP32_set

#thingspeak 設定
mq_server = 'thingspeak SERVER'#thingspeak SERVER
mq_id = 'id number' #thingspeak格式ID
mq_topic= 'channels/' + 'channel number' + '/publish'#thingspeak 伺服器topic格式
mq_user = 'user account'  #thingspeak account
mq_pass = 'password' #thingspeak password
mqClient0 = MQTTClient(mq_id,mq_server,user=mq_user,password=mq_pass,keepalive=60)
mqClient0.connect(False)


#Blynk設定
token ='Blynk token'# Blynk token
blynk = BlynkLib.Blynk(token)            # 取得 Blynk object


#感測器及腳位設定
soil_Moisture = 39
dht_power = 32
water_Level = 36
water_valve = 33
d22 = 14
EMI_Pin = 35
BASE_Pin = 22
sen_max_V = 3.3
sen_min_V = 0.85
sen_sample = 200


ESP32_S = ESP32_set.Pin_set(soil_Moisture,dht_power,water_Level,water_valve,d22,EMI_Pin,BASE_Pin,sen_max_V,sen_min_V,sen_sample)


def v0_handler(value):             # 從 V0 虛擬腳位讀取手機按鈕狀態的函式
    value(int(value[0]))
    blynk.on("V0", v0_handler)     # 註冊由 v0_handler 處理 V0 虛擬腳位

def d22_handler():            					# 回應 Blynk 讀取 V1/V3 虛擬腳位的函式
    temp , humidity = ESP32_S.box_status()      # DHT22開始量測box status
    blynk.virtual_write(1, str(temp)) #讀取溫度
    blynk.virtual_write(3, str(humidity)) #讀取溼度

def v2_handler():				# 提供soil moisture電壓到V2的函式
    blynk.virtual_write(2, '{}'.format(ESP32_S.soil_moisture_sen()))

def v4_handler(value):             # 從 V4 虛擬腳位讀取手機按鈕狀態的函式
    ESP32_S.BASE_pin.value(int(value[0]))
    blynk.on("V4",v4_handler)          # 註冊由 v4_handler 處理 V4 虛擬腳位

def v5_handler():             # 提供water level sensor電壓到V2的函式
    blynk.virtual_write(5, '{}'.format(ESP32_S.water_Level))

def LED_handler():				# 定義土壤乾燥指示燈的函式
    if ESP32_S.soil_moisture_sen()>50:
        blynk.virtual_write(6,255)
        blynk.virtual_write(7,0)
    else:
        blynk.virtual_write(6,0)
        blynk.virtual_write(7,255)

def thingspeak_update():
    temp , humidity = ESP32_S.box_status()
    mq_message='field1=' + '{}'.format(ESP32_S.soil_moisture_sen()) + '&field2=' + str(temp) + '&field3=' + str(humidity)  
    #上面這行是thingspeak表格格式+感測器讀值
    mqClient0.publish(mq_topic,mq_message)

def wifi_connect_check():
    if wifi.isconnected():
        blynk.virtual_write(9, 'wifi連接成功，信號強度:'+ str(wifi.status('rssi')))
    else:
        wifi.connect('ASUS_20_2G','sum998888')
        blynk.virtual_write(9, 'retry connect wifi')


timer = BlynkTimer()               # 建立計時器管理物件
timer.set_interval(5, d22_handler)  # 建立每5秒觸發的計時器
timer.set_interval(5, v2_handler)  # 建立每5秒觸發的計時器
timer.set_interval(5, v5_handler)  # 建立每5秒觸發的計時器
timer.set_interval(5, LED_handler)  # 建立每5秒觸發的計時器
timer.set_interval(5, wifi_connect_check)# 建立每5秒觸發的計時器
timer.set_interval(21, thingspeak_update)  # 建立每5秒觸發的計時器

try:
    while True:
        gc.collect()
        blynk.run()
        timer.run()
        ESP32_S.water_valve_OC_controller()

except Exception as e:
    blynk.log_event("error_code",str(e))
    machine.reset()
