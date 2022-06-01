# Weather Station API is the main code that operates the station operations.
# It acts as a server to dish out information to the web application.
# It also receives information from the physical sensors, as well as from OpenWeatherMap.org.
# If the server is not working with an error code about not detecting the BME280 module, restart the RPi and
# reload the weatherStationAPI.py code.
from flask import Flask
import json
from flask_cors import CORS
import requests
from adafruit_bme280 import basic as adafruit_bme280
import board
import digitalio

# Imports for windspeed counting
import time, sys, threading
from datetime import datetime
import RPi.GPIO as GPIO

# variables for windspeed
count = 0
windSpeed = 0

# Set up Pin 40 (GPIO21) as input.
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Define my_callback function to count reed switch closures
# per period.
def my_callback(channel):
    if GPIO.input(21):
        global count
        count = count + 1
        #print('Rising edge detected on pin 40')
        #print(count)

# Define clearCount function to print the windspeed, time,
# and then clear the counter.
def clearCount():
    global count
    global windSpeed
    print(count)
    windSpeed = round( count * (0.2/0.2984), 2)
    print(str(round( count * (0.2/0.2984), 2)) + " MPH")
    print(datetime.now().strftime('%H:%M:%S'))
    count = 0
    threading.Timer(5.0, clearCount).start()


#main Flask app
app = Flask("app")
CORS(app)

print('This ran!')

@app.route("/")
def weatherIndicated():
    print('This Also Ran!')
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?zip=16602,us&appid=431d09d780e3c761a8589f7bd5273fe0&units=imperial"
    )
    weather = response.json()
    # print(weather)

    # Sensor data from BME280, using SPI for wiring.
    spi = board.SPI()
    cs = digitalio.DigitalInOut(board.D5)
    bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)

    while True:
        bme280.sea_level_pressure = bme280.pressure + 42.684
        data = {
            "realTemp": (bme280.temperature * (9 / 5)) + 32,
            "feelsLike": weather["main"]["feels_like"],
            "humidity": bme280.relative_humidity,
            "windSpeed": windSpeed,
            "sky": weather["weather"][0]["main"],
            "airPressure": bme280.pressure * 0.0145037738,
            "altitude": bme280.altitude
        }
        print("Data Accessed")
        # time.sleep(5)
        return json.dumps(data)

GPIO.add_event_detect(21, GPIO.RISING, callback=my_callback)
clearCount()


app.run(host="0.0.0.0", port=8080)
