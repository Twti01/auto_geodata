#!/usr/bin/python

import time
import RPi.GPIO as GPIO

#definiere LED Pin
led_pin = 26

#setze GPIO Modus auf GPIO.BOARD	
GPIO.setmode(GPIO.BCM)
#lege Pin als Ausgang fest
GPIO.setup(led_pin, GPIO.OUT)


def run(cnt=5,brk=1):
    for i in range(cnt):
        GPIO.output(led_pin, GPIO.HIGH)      
        time.sleep(brk)                         
        GPIO.output(led_pin, GPIO.LOW)       
        time.sleep(brk)
        
if __name__ == "__main__":
    run()
    GPIO.cleanup()

#try:
	#while True:
		#LED an
	#	GPIO.output(led_pin, GPIO.HIGH)
		#warte 0,2 Sekunden
	#	time.sleep(0.2)
		#LED aus
	#	GPIO.output(led_pin, GPIO.LOW)
		#warte 0,2 Sekunden
	#	time.sleep(0.2)

#except KeyboardInterrupt:
	#STRG+C zum Beenden des Programms
#	GPIO.cleanup()
