#Qing Yu (qy95), Weiran Wang (ww463), Lab1, 9/11/2018
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.2)
    if (not GPIO.input(17)):
        print(" ")
        print "Button 17 pressed..."