from machine import ADC,Pin
import dht,statistics,machine

class Pin_set:
    #感測器及繼電器腳位設定,腳位設定依實際狀況設定
    #sen_max_V為土壤溼度感測器最乾燥的電壓,sen_min_V 為土壤溼度感測器最濕潤的電壓,由實驗得來
    def __init__(self,soil_Moisture,dht_power,water_Level,water_valve,d22,EMI_Pin,BASE_Pin,sen_max_V,sen_min_V,sen_sample):
        self.soil_Moisture = soil_Moisture
        self.dht_power = dht_power
        self.water_Level= water_Level
        self.water_valve = water_valve
        self.d22 = d22
        self.EMI_Pin = EMI_Pin
        self.BASE_Pin = BASE_Pin
        self.sen_max_V = sen_max_V
        self.sen_min_V = sen_min_V
        self.sen_sample = sen_sample
        self.sen_coff = (100/(sen_max_V-sen_min_V))
        
        soil_M_pin = ADC(Pin(soil_Moisture))
        soil_M_pin.atten(ADC.ATTN_11DB)
        soil_M_pin.width(ADC.WIDTH_12BIT)
        dht_P_pin = Pin(dht_power,Pin.OUT)
        d22_D_pin = dht.DHT22(Pin(d22)) 
        water_L_pin = ADC(Pin(water_Level))
        water_L_pin.atten(ADC.ATTN_11DB)
        water_L_pin.width(ADC.WIDTH_12BIT)
        water_V_pin = Pin(water_valve,Pin.OUT)
        EMI_pin = ADC(Pin(EMI_Pin))
        EMI_pin.atten(ADC.ATTN_11DB)
        EMI_pin.width(ADC.WIDTH_12BIT)
        BASE_pin = Pin(BASE_Pin,Pin.OUT)
    
    def soil_moisture_sen(self,soil_M_pin,sen_min_V,sen_coff):
        soil_moisture_list=[]
        i=0
        for i in range(self.sen_sample):#設定取樣範圍
            soil_moisture_val=(((soil_M_pin/4095*3.3)-sen_min_V)*sen_coff)#將電壓轉換為乾度%, over:3.3,全濕:0.85V, 空氣約2.15v
            soil_moisture_list.append(soil_moisture_val)
            time.sleep(0.01)
        soil_moisture_medi=statistics.median(soil_moisture_list)#計算中位數
        return soil_moisture_medi
