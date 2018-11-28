#Qing Yu (qy95), Weiran Wang (ww463), Lab1, 9/11/2018
import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def GPIO17_callback(channel):
    print(" ")
    print "Pause"
    cmd = "echo pause > /home/pi/video_fifo"
    print subprocess.check_output(cmd, shell=True)
        
def GPIO22_callback(channel):
    print(" ")
    print "Forward 10 seconds"
    cmd = "echo seek +10 > /home/pi/video_fifo"
    print subprocess.check_output(cmd, shell=True)

def GPIO23_callback(channel):
    print(" ")
    print "Rewind 10 seconds"
    cmd = "echo seek -10 > /home/pi/video_fifo"
    print subprocess.check_output(cmd, shell=True)

def GPIO19_callback(channel):
    print(" ")
    print "Rewind 10 seconds"
    cmd = "echo seek -30 > /home/pi/video_fifo"
    print subprocess.check_output(cmd, shell=True)

def GPIO26_callback(channel):
    print(" ")
    print "Rewind 10 seconds"
    cmd = "echo seek +30 > /home/pi/video_fifo"
    print subprocess.check_output(cmd, shell=True)
    
GPIO.add_event_detect(17,GPIO.FALLING, callback=GPIO17_callback)
GPIO.add_event_detect(22,GPIO.FALLING, callback=GPIO22_callback)
GPIO.add_event_detect(23,GPIO.FALLING, callback=GPIO23_callback)
GPIO.add_event_detect(19,GPIO.FALLING, callback=GPIO19_callback)
GPIO.add_event_detect(16,GPIO.FALLING, callback=GPIO16_callback)

    Try:
        print(" ")
        print "Waiting for #27 button pressed and Quit"
        GPIO.wait_for_edge(27,GPIO.FALLING)
        cmd = "echo quit > /home/pi/video_fifo"
        print subprocess.check_output(cmd, shell=True)
    except KeyboardInterrupt:
        GPIO。cleanup()
    GPIO.cleanup()
        
        
