ESP32-Automatic-sprinkler
==========================
Use PYTHON to control ESP32 with soil moisture meter/water level meter and other sensors to control the water valve switch to complete the automatic watering function. Cooperate with open source software such as BLYNK/THINGSPEAK to complete the mobile phone monitoring function.

How to use this package
==========================
1.ESP32_set.py
--------------------------
define ESP32 Pin set & sensor function for Capacitive Soil Moisture Sensor/water Level sensor/DHT22

Pin definition for this project
soil_Moisture = 39         # soil sensor signal Pin<br/>
dht_power = 32             # DHT22 power Pin<br/>
water_Level = 36           # water Level sensor signal Pin<br/>
water_valve = 33           # send signal to control relay<br/>
d22 = 14                   # DHT22 data Pin<br/>
EMI_Pin = 35<br/>        
BASE_Pin = 22<br/>
sen_max_V = 3.3            # soil sensor signal Max voltage<br/>    
sen_min_V = 0.85           # soil sensor signal LOW voltage(in water)<br/>
sen_sample = 200           # data sample for calculate median<br/>

Parts
==========================

ESP32
--------------------------
<img src="https://github.com/tyhsup/ESP32-Automatic-sprinkler/raw/main/photo/ESP32.jpg" width='30%' height='30%'>

Capacitive Soil Moisture Sensor
--------------------------
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

