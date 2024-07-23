#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import board

#from Adafruit_LED_Backpack import SevenSegment
from adafruit_ht16k33.segments import Seg7x4

i2c = board.I2C()
segment2 = Seg7x4(i2c, address=0x70) #segment der I2C Adresse 0x70 und die Displaydefinition zuweisen

segment2.fill(0) # Initialisierung des Displays. Muss einmal ausgeführt werden bevor das Display benutzt wird.

print ("STRG+C Druecken zum beenden.") #print Befehl für Ausgabe zum beenden des Scriptes

def run():
    segment2.fill(0)
    segment2.show()




