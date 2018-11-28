#Qing Yu (qy95), Weiran Wang (ww463), Lab1, 9/11/2018
import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.2)
    if (not GPIO.input(17)):
        print(" ")
        print "Pause"
        cmd = "echo pause > /home/pi/video_fifo"
        print subprocess.check_output(cmd, shell=True)
        
    if (not GPIO.input(22)):
        print(" ")
        print "Forward 10 seconds"
        cmd = "echo seek +10 > /home/pi/video_fifo"
        print subprocess.check_output(cmd, shell=True)
        
    if (not GPIO.input(23)):
        print(" ")
        print "Rewind 10 seconds"
        cmd = "echo seek -10 > /home/pi/video_fifo"
        print subprocess.check_output(cmd, shell=True)
        
    if (not GPIO.input(27)):
        print(" ")
        print "Quit"
        cmd = "echo quit > /home/pi/video_fifo"
        print subprocess.check_output(cmd, shell=True)
        break
        
        
