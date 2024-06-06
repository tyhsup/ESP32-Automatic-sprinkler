ESP32-Automatic-sprinkler
==========================
Use PYTHON to control ESP32 with soil moisture meter/water level meter and other sensors to control the water valve switch to complete the automatic watering function. Cooperate with open source software such as BLYNK/THINGSPEAK to complete the mobile phone monitoring function.

How to use this package
==========================
ESP32_set.py
--------------------------
this file efine ESP32 Pin set & sensor function for Capacitive Soil Moisture Sensor/water Level sensor/DHT22<br/>
from this file you can declare "Pin_set" Class object<br/>

EXP: input ESP32 GPIO Pin & parameter & sample number for improve soil Moisture sensor data<br/>
soil_Moisture = 39         # soil sensor signal Pin<br/>
dht_power = 32             # DHT22 power Pin<br/>
water_Level = 36           # water Level sensor signal Pin<br/>
water_valve = 33           # send signal to control relay<br/>
d22 = 14                   # DHT22 data Pin<br/>
EMI_Pin = 35<br/>        
BASE_Pin = 22<br/>
sen_max_V = 3.3            # soil sensor signal Max voltage(transfer data from voltage to percentage)<br/>    
sen_min_V = 0.85           # soil sensor signal LOW voltage((transfer data from voltage to percentage))<br/>
sen_sample = 200           # soil_Moisture data sample for calculate median<br/>

ESP32_S = ESP32_set.Pin_set(soil_Moisture,dht_power,water_Level,water_valve,d22,EMI_Pin,BASE_Pin,sen_max_V,sen_min_V,sen_sample)<br/>

Class Pin_set include some function for soil moisture/environment temperature and humidity/water level measurement

Parts
==========================

ESP32
--------------------------
<img src="https://github.com/tyhsup/ESP32-Automatic-sprinkler/raw/main/photo/ESP32.jpg" width='30%' height='30%'>

Capacitive Soil Moisture Sensor
--------------------------
I'm use this parts to define soil moisture content by voltage in water and full output voltage<br/>
<img src="https://github.com/tyhsup/ESP32-Automatic-sprinkler/raw/main/photo/Capacitive-Soil-Moisture-Sensor.jpg" width='30%' height='30%'>

water Level sensor
--------------------------
<img src="https://github.com/tyhsup/ESP32-Automatic-sprinkler/raw/main/photo/Water-Level-Sensor.jpg" width='30%' height='30%'>

<img src="https://github.com/tyhsup/ESP32-Automatic-sprinkler/raw/main/photo/Water-Level-Sensor-Pinout.jpg" width='30%' height='30%'>

relay
--------------------------
<img src="https://github.com/tyhsup/ESP32-Automatic-sprinkler/raw/main/photo/relay.png" width='30%' height='30%'>

water valve
--------------------------
<img src="https://github.com/tyhsup/ESP32-Automatic-sprinkler/raw/main/photo/water-valve.jpg" width='30%' height='30%'>

