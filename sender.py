import paho.mqtt.client as mqtt 
import string
import random
import datetime
import json
import time
import RPi.GPIO as GPIO
import dht11
from light_sensor import LightSensor

random_name = "".join(random.choices(string.ascii_letters + string.digits, k=10))
client = mqtt.Client(client_id=random_name , clean_session=True)
sensor = LightSensor()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin = 4)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connection successful")
    elif rc == 1:
        print("connection refused - incorrect protocol version")
    elif rc == 2:
        print("connection refused - invalid client identifier")
    elif rc == 3:
        print("connection refused - server unavailable")
    elif rc == 4:
        print("connection refused - username or/and password incorrect")
    elif rc == 5:
        print("connection refused - not authorised")
    else:
        print(f"connection refused: {rc}")
        
def on_disconnect(client, userdata, rc):
    print(f"disconnected from server with result code: {rc}")

#dummy data worker
def worker(client, interval):
    while True:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        temp = 20.0 + random.random()
        hum = 40.0 + random.random()
        data = {'ts' : ts, 'temp' : temp, 'hum' : hum}    
        client.publish("RPi/GR6/dht11", payload=json.dumps(data))
        time.sleep(interval)

def dht(client, interval):
    while True:
        light = sensor.readLight()
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        result = instance.read()
        while not result.is_valid():  # read until valid values
            result = instance.read()
        data = {'ts' : ts, 'temp' : result.temperature, 'hum' : result.humidity}    
        data2 = {'light': light}    
        client.publish("RPi/GR6/dht11", payload=json.dumps(data))
        client.publish("RPi/GR6/light_sens", payload=json.dumps(data2))
        time.sleep(interval)






client.on_connect = on_connect 
client.on_disconnect = on_disconnect


client.connect("mqtt-dashboard.com", 1883)
client.loop_start()
dht(client, 1)
