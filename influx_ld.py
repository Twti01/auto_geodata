import influxdb
import datetime
import random
import time
import threading

import RPi.GPIO as GPIO
import dht11
from light_sensor import LightSensor

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin = 4)

db = influxdb.InfluxDBClient(host="127.0.0.1", port=8086, username="linnart", password="linnart")

print("connection to influxdb done!")

db.switch_database("db_damm")

print("DB aktiv")

def worker(sensor_name, sensor_type, temp, humid, light, interval):
    while True:
        data = {
            "measurement": "env",
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tags": {
                "owner": "linnart",
                "name": sensor_name,
                "type": sensor_type,
            },
            "fields": {
                "temp": temp,
                "humid": humid,
                "light": light
            }
        }
        print(data)
        if not db.write_points([data]):
            print("error write points!")
        time.sleep(interval)

sensor = LightSensor()

while True:
    result = instance.read()
    light = sensor.readLight()
    while not result.is_valid():  # read until valid values
        result = instance.read()
        temp = result.temperature
        humid = result.humidity
        for i in range (result.is_valid()):
            threading.Thread(target=worker, args=("S1", "DHT-11", temp, humid, light, 5)).start()
#threading.Thread(target=worker, args=("S1", "DHT-11", "BHT", 20.0, 45.0, 5)).start()
#threading.Thread(target=worker, args=("S2", "DHT-11", "TU", 22.0, 50.0, 10)).start()