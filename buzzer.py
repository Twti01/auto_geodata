#!/usr/bin/python

import RPi.GPIO as GPIO         #importieren der benoetigten Bibliotheken
import time

buzzer_pin = 18                 #buzzer_pin wird definiert

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

def run(cnt=1,brk=1):
    for i in range(cnt):
        GPIO.output(buzzer_pin, GPIO.HIGH)     #Gebe Geraeusch aus
        time.sleep(brk)                        #warte eine halbe Sekunde
        GPIO.output(buzzer_pin, GPIO.LOW)      #Stoppe Geraeuschausgabe
        time.sleep(brk)

if __name__ == "__main__":
    run()
    GPIO.cleanup()
