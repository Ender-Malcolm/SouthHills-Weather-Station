# SouthHills-Weather-Station
The API-Flask server on a Raspberry Pi, which serves weather data from sensor inputs. 

  Greetings, and welcome to the code repository for SouthHills Weather Station. This code runs on a Raspberry Pi 4, and provides current weather data to a front end web application. The sensors chosen were a BME280 Pressure/Humidity/Temperature package, and a SparkFun Weather Station Kit. The latter includes three (3) analogue sensors, an anemometer, wind vane, and rain gauge. These sensors use reed switches and magnets on rotating armatures to create an event on the RPi's GPIO pins. Currently only the Anemometer is hooked up, and thus code for the other two analogue sensors is not included.

  If you are interested in using this code, you will need an account on OpenWeatherMap.com, and will have to sign up for the API Key on the Current Weather Data. Replace the included location, API Key, and units with your own, and you will be able to recieve some basic conditions from your local area. You will require sensors and an RPi to properly duplicate the full use of this code.
