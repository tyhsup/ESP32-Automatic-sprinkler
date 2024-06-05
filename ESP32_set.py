from machine import ADC,Pin
import dht,statistics,time,gc

class Pin_set:
    #感測器及繼電器腳位設定,腳位設定依實際狀況設定
    #sen_max_V為土壤溼度感測器最乾燥的電壓,sen_min_V 為土壤溼度感測器最濕潤的電壓,由實驗得來
    def __init__(self,soil_Moisture,dht_power,water_Level,water_valve,d22,EMI_Pin,BASE_Pin,sen_max_V,sen_min_V,sen_sample):
        self.soil_M_pin = ADC(Pin(soil_Moisture))
        self.soil_M_pin.atten(ADC.ATTN_11DB)
        self.soil_M_pin.width(ADC.WIDTH_12BIT)
        self.dht_P_pin = Pin(dht_power,Pin.OUT)
        self.d22_D_pin = dht.DHT22(Pin(d22))
        self.water_L_pin = ADC(Pin(water_Level))
        self.water_L_pin.atten(ADC.ATTN_11DB)
        self.water_L_pin.width(ADC.WIDTH_12BIT)
        self.water_V_pin = Pin(water_valve,Pin.OUT)
        self.EMI_pin = ADC(Pin(EMI_Pin))
        self.EMI_pin.atten(ADC.ATTN_11DB)
        self.EMI_pin.width(ADC.WIDTH_12BIT)
        self.BASE_pin = Pin(BASE_Pin,Pin.OUT)
        self.sen_max_V = sen_max_V
        self.sen_min_V = sen_min_V
        self.sen_sample = sen_sample
        self.sen_coff = (100/(sen_max_V-sen_min_V))
    
    def soil_moisture_sen(self):
        soil_moisture_list=[]
        i=0
        for i in range(self.sen_sample):#設定取樣範圍
            soil_moisture_val=(((self.soil_M_pin.read()/4095*self.sen_max_V)-self.sen_min_V)*self.sen_coff)#將電壓轉換為乾度%, over:3.3,全濕:0.85V, 空氣約2.15v
            soil_moisture_list.append(soil_moisture_val)
            time.sleep(0.01)
        soil_moisture_medi=statistics.median(soil_moisture_list)#計算中位數
        return soil_moisture_medi
    
    def water_Level(self):
        water_Level_val=(self.water_L_pin.read()/4095*self.sen_max_V)#讀取water level sensor電壓值
        return water_Level_val
    
    def EMI_Pin_val(self):
        EMI_Pin_val=(self.EMI_pin.read()/4095*self.sen_max_V)
        return EMI_Pin_val
    
    def water_valve_OC_controller(self):
        if self.soil_moisture_sen()>50:
            if self.water_Level == 0:
                self.water_V_pin.value(1)
            else:
                self.water_V_pin.value(0)
        else:
            self.water_V_pin.value(0)
            
    def box_status(self):
        gc.collect()
        self.dht_P_pin.init()
        self.dht_P_pin.value(True)
        time.sleep(2)
        self.d22_D_pin.measure()
        temp = self.d22_D_pin.temperature()
        humidity = self.d22_D_pin.humidity()
        self.dht_P_pin.value(False)
        return temp , humidity
        

