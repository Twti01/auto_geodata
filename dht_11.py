import RPi.GPIO as GPIO
import dht11
#import blinking_led
#import buzzer
#import vibration
#import segment2
import sqlite3
import datetime


conn = sqlite3.connect("example.sqlite")
sql = "CREATE TABLE IF NOT EXISTS dht11 (id INTEGER PRIMARY KEY NOT NULL,  timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, temp REAL NOT NULL, humid REAL NOT NULL)"

try:
    conn.execute(sql)
    conn.commit()
    print("table created!")
except sqlite3.Error as err:
    print(err)
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)




# read data using pin 14
instance = dht11.DHT11(pin = 4)


while True:
    result = instance.read()
    while not result.is_valid():  # read until valid values
        result = instance.read()
        temp = result.temperature
        humid = result.humidity
        for i in range (result.is_valid()):
            sql = f"INSERT INTO dht11 (timestamp, temp, humid) VALUES (CURRENT_TIMESTAMP, {temp: .3f}, {humid: .3f})"
            try:
                conn.execute(sql)
            except sqlite3.Error as err:
                print(err)
        conn.commit()
        try:
            cursor = conn.execute(sql)
        except sqlite3.Error as err:
            print(err)
        sql = "SELECT id, timestamp, temp, humid FROM dht11 WHERE id <= 1000"
    try:
       cursor = conn.execute(sql)
    except sqlite3.Error as err:
       print(err)

    for row in cursor:
        pass#print(row)
    #print(temp, humid)
    if result.humidity > 50.0:
        pass
        #blinking_led.run()
        #buzzer.run()
        #vibration.run()
        #segment2.run()
        
    print(f"Temp: {result.temperature:.3f} C, humid: {result.humidity:.3f}")

