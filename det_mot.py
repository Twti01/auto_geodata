import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd 
from light_sensor import LightSensor

GPIO.cleanup()

motion_pin = 23
buzzer_pin = 18

lcd_columns = 16
lcd_rows = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(motion_pin, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.output(buzzer_pin, GPIO.LOW) #GPIO.HIGH soll Buzzer initial anschalten, während GPIO.LOW soll Buzzer initial ausschalten

i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, 0x21)

sensor = LightSensor()
log_lst = []

try: 
    while True:
        light = sensor.readLight()

        if(GPIO.input(motion_pin) == 1):
            log_lst.append(f"Motion detected, Light level: {light}")
            lcd.message="Motion"
            GPIO.output(buzzer_pin, GPIO.HIGH) 
            time.sleep(0.5) 
            GPIO.output(buzzer_pin, GPIO.LOW) 
        
        elif(GPIO.input(motion_pin) == 0):
            log_lst.append(f"No Motion detected, Light level: {light}")
            lcd.backlight = True
            lcd.message = "No\nMotion"
            time.sleep(3)
            lcd.clear()             #schauen ob lcd clear geht


except KeyboardInterrupt:
    GPIO.cleanup()


with open("log.file", "w") as f:
    for lines in log_lst:
        f.write(f"{lines}\n")