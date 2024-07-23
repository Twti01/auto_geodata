import paho.mqtt.client as paho
import influxdb
import json
import RPi.GPIO as GPIO
import datetime
import dht11
from light_sensor import LightSensor
import time
import math
import threading
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps_v3 import BrickletGPSV3

host = "172.16.231.188"
port = 8086
username = "linnart"
password = "linnart"
HOST = "localhost"
PORT = 4223
UID_GPS = "21LD"  #über BrickViewer finden

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=4)
TRIG = 16
ECHO = 12

# InfluxDB-Einstellungen
db = influxdb.InfluxDBClient(host=host, port=port, username=username, password=password)
db.switch_database('db_damm')

print("Connection to db successful")

# MQTT-Einstellungen
mqtt_broker = "mqtt-dashboard.com"
mqtt_topic = "RPi/GR6/#"

GPIO.setup(TRIG, GPIO.OUT)  # Variable TRIG als Output festlegen.
GPIO.setup(ECHO, GPIO.IN)   # Variable ECHO als Input festlegen.

# Initialize GPS
ipcon = IPConnection()
gps = BrickletGPSV3(UID_GPS, ipcon)
latitude = 0.0
longitude = 0.0
gps_lock = threading.Lock()

# Callback-Funktion für GPS-Daten
def cb_coordinates(latitude, ns, longitude, ew):
    global lat, lon
    with gps_lock:
        lat = latitude / 1000000.0 * (1 if ns == 'N' else -1)
        lon = longitude / 1000000.0 * (1 if ew == 'E' else -1)

# Verbinde zur Tinkerforge IP Connection
def connect_to_gps():
    ipcon.connect(HOST, PORT)
    gps.register_callback(gps.CALLBACK_COORDINATES, cb_coordinates)
    gps.set_coordinates_callback_period(1000)

connect_to_gps()

def on_message(client, userdata, message):
    payload = message.payload.decode()
    topic = message.topic

    # Debugging-Ausgabe
    print(f"Received message on topic {topic}: {payload}")

    try:
        sensor = LightSensor()
        result = instance.read()
        light = sensor.readLight()
        
        while not result.is_valid():  # read until valid values
            result = instance.read()

        temp = result.temperature
        humid = result.humidity
        distance = measure()
        
        data = [{
            "measurement": "environment",
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tags": {
                "host": "raspberrypi",
                "owner": "linnart",
            },
            "fields": {
                "temp": float(temp),
                "light": float(light),
                "humid": float(humid),
                "distance": float(distance),
            }
        }]
        db.write_points(data)
        
        with gps_lock:
            lat = latitude
            lon = longitude
            data2 = [{
                "measurement": "coordinates",
                "time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "tags": {
                    "host": "raspberrypi",
                    "owner": "linnart",
                },
                "fields": {
                    "latitude": float(lat),
                    "longitude": float(lon),
                }
            }]
        db.write_points(data2)
        print("Data written to InfluxDB")
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Nachricht: {e}")

def measure():
    GPIO.output(TRIG, True)  # Sendet ein Ultraschallsignal
    time.sleep(0.00001)  # Wartet 0,00001 Sekunden
    GPIO.output(TRIG, False)  # Beendet das Senden des Ultraschallsignals

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

# MQTT-Client einrichten
mqtt_client = paho.Client()
mqtt_client.on_message = on_message

# Verbindung herstellen und abonnieren
mqtt_client.connect(mqtt_broker)
mqtt_client.subscribe(mqtt_topic)

# Start the MQTT loop
mqtt_client.loop_start()

# Keep the program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.loop_stop()
    ipcon.disconnect()
