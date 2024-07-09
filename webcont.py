from flask import Flask, redirect, render_template, request, url_for, request, redirect
import RPi.GPIO as GPIO
import time
import dht11
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd 
import sqlite3
from light_sensor import LightSensor

app = Flask(__name__)

act_pins = (18, 26, 24)
other_pins = (13, 5, 18)

def execute(sql):
    conn = sqlite3.connect("nightsens.sqlite")
    try:
        result = conn.execute(sql)
        conn.commit()
        return result
    except sqlite3.Error as err:
        print(err)
        return None

def setupGPIO_out(index):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(act_pins[index], GPIO.OUT)

def setupGPIO_in(index):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(act_pins[index], GPIO.IN)
    
def setupGPIO_board(index):
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setwarnings(False)
    GPIO.setup(other_pins[index], GPIO.OUT)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/button')
def button():
    setupGPIO_in(1)
    GPIO.cleanup()
    return render_template('index.html')

@app.route('/dht11')
def dht():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    instance = dht11.DHT11(pin = 4)
    
    while True:
        result = instance.read()
        while not result.is_valid():  # read until valid values
            result = instance.read()
            temp = result.temperature
            humid = result.humidity
    return render_template('index.html')

@app.route('/vibration')
def vibration():
    setupGPIO_board(0)
    GPIO.output(other_pins[0], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(other_pins[0], GPIO.LOW)
    GPIO.cleanup()
    return render_template('index.html')

@app.route('/buzzer') 
def buzzer():
    setupGPIO_out(0)
    for i in range(1,10):
        GPIO.output(act_pins[0], GPIO.HIGH)
        time.sleep(1)
        GPIO.output(act_pins[0], GPIO.LOW)
        time.sleep(1)
        GPIO.cleanup()
        return render_template('index.html')

@app.route('/lcd')
def lcd():
    lcd_columns = 16
    lcd_rows = 2
    i2c = busio.I2C(board.SCL, board.SDA)
    lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, 0x21)
    lcd.message = "Active"
    time.sleep(10)
    lcd.clear()
    lcd.backlight = False
    GPIO.cleanup()
    return render_template('index.html')  

@app.route('/nightsens', methods=['POST'])  
def nightsens():
    setupGPIO_in(2)
    execute("""CREATE TABLE IF NOT EXISTS sleep_noises (
            id INTEGER PRIMARY KEY NOT NULL,
            sound VARCHAR(255),
            temperature FLOAT,
            humidity FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            light FLOAT
            """)
    while True:
        sensor = LightSensor()
        result = instance.read()
        instance = dht11.DHT11(pin=4)
        light = sensor.readLight()
        if(GPIO.input(act_pins[2])==GPIO.LOW):
            sound = "Noise detected!"
        else:
            sound = "No noise detected!"
        
        while not result.is_valid():  # read until valid values
            result = instance.read()
            temp = result.temperature
            humid = result.humidity

        execute("""
                INSERT INTO sleep_noises (sound, temperature, humidity, light)
                VALUES (%s, %s, %s, %s)""", (sound, temp, humid, light)) 
    
        return render_template('nightsens.html')


@app.route('/nightsens', methods=['GET'])
def show_table():
    result = execute("SELECT * FROM sleep_noises")
    return render_template('nightsens.html')

if __name__ == '__main__':
    app.run(host="192.168.178.118", port=8000, debug=True)
    GPIO.cleanup()
