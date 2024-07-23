import influxdb
import datetime
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
TRIG = 16
ECHO = 12

db = influxdb.InfluxDBClient(host="127.0.0.1", port=8086, username="linnart", password="linnart")

print("connection to influxdb done!")

GPIO.setup(TRIG,GPIO.OUT) # Variable TRIG als Output festlegen.
GPIO.setup(ECHO,GPIO.IN) # Variable ECHO als Input festlegen.

db.switch_database("abschluss_PI")

print("DB aktiv")

def worker(sensor_name, sensor_type, interval):
    while True:
        sensor = LightSensor()
        result = instance.read()
        light = sensor.readLight()
            
        while not result.is_valid():  # read until valid values
            result = instance.read()
            temp = result.temperature
            humid = result.humidity
        temp = result.temperature
        humid = result.humidity
        distance = measure()
        data = {
            "measurement": "pi_final",
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tags": {
                "owner": "linnart",
                "name": sensor_name,
                "type": sensor_type,
            },
            "fields": {
                "temp": float(temp),
                "humid": float(humid),
                "light": float(light),
                "distance": float(distance),
            }
        }
        print(data)
        if not db.write_points([data]):
            print("error write points!")
        time.sleep(interval)



def measure():
    #GPIO.output(TRIG, False)
    #time.sleep(2) # 2 Sekunden Wartezeit.

    GPIO.output(TRIG, True) # Sendet ein Ultraschallsignal
    time.sleep(0.00001) # Wartet 0,00001 Sekunden
    GPIO.output(TRIG, False) # Beendet das senden des Ultraschallsignals
        
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 
    distance = round(distance, 2)
    return distance 



threading.Thread(target=worker, args=("Raspberry-Pi", "DHT-11, light, distance", 5)).start()