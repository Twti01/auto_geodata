#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# definieren des Vibrationspins
vibration_pin = 27

# setze Boardmodus zu GPIO.BOARD
GPIO.setmode(GPIO.BCM)

# lege Vibrationspin als Ausgang fest
GPIO.setup(vibration_pin, GPIO.OUT)

def run(cnt=1,brk=1):
    for i in range(cnt):
        GPIO.output(vibration_pin, GPIO.HIGH)      
        time.sleep(brk)                         
        GPIO.output(vibration_pin, GPIO.LOW)       
        time.sleep(brk)


if __name__ == "__main__":
    run()
    GPIO.cleanup()


# schalte Vibration ein
#GPIO.output(vibration_pin, GPIO.HIGH)
# warte eine Sekunde
#time.sleep(1)
# schalte Vibration aus
#GPIO.output(vibration_pin, GPIO.LOW)

#GPIO.cleanup()
