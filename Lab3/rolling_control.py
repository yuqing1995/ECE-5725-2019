rolling_control_v4.py
Today
4:09 PM

Weiran Wang uploaded an item
Text
rolling_control_v4.py
import pygame
from pygame.locals import* #for event MOUSE variables
import os
import time
import RPi.GPIO as GPIO
import math

#os.putenv('SDL_VIDEODRIVER', 'fbcon') #Display on piTFT
#os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB') #Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

pygame.init()
#pygame.mouse.set_visible(False)
pygame.mouse.set_visible(True)

size = width, height = 320, 240 #set up screen size
WHITE = 255,255,255 #define color variables
BLACK = 0,0,0
screen = pygame.display.set_mode(size)


my_font = pygame.font.Font(None,20)
center_button = 'STOP'
left_state=['Stop','Stop','Stop']
right_state = ['Stop','Stop','Stop']
time_state_left = ['0','0','0']
time_state_right = ['0','0','0']
my_buttons = {'Quit':(240,220), center_button:(150,110),"Left History":(50,20),"Right History":(260,20)}




GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def direction(servo,dir):
    if dir == "clockwise":
        servo.ChangeFrequency(46.73)
        servo.ChangeDutyCycle(6.54)
    if dir == "counter-clockwise":
        servo.ChangeFrequency(46.3)
        servo.ChangeDutyCycle(7.41)
    if dir == "stop":
        servo.ChangeDutyCycle(0)

def display_left(left_s):
    left_state[2] = left_state[1]
    left_state[1]= left_state[0]
    left_state[0] = left_s
    t= "%.3g" %(time.time()-start_servo)
    time_state_left[2] = time_state_left[1]
    time_state_left[1] = time_state_left[0]
    time_state_left[0] = str(t)

def display_right(right_s):
    right_state[2] = right_state[1]
    right_state[1] = right_state[0]
    right_state[0] = right_s
    t1= "%.3g" %(time.time()-start_servo)
    time_state_right[2] = time_state_right[1]
    time_state_right[1] = time_state_right[0]
    time_state_right[0] = str(t1)

#if start_flag == 0:
p = GPIO.PWM(5, 46.5)
p2 = GPIO.PWM(6, 46.5)
##dc = 6.977
p.start(6.977)
##dc2 = 6.977
p2.start(6.977)

start_servo = time.time()
count_left = 0
count_right = 0
count_time_left = 0
count_time_right = 0
#start_flag = 0
flag = 0
start = time.time()
resume_flag = 0
count_l = 0
count_r = 0

def GPIO17_callback(channel):
        global  count_l
        count_l= 1
        display_left('Clkwise')
        direction(p,"clockwise")
       

def GPIO22_callback(channel):
        global  count_l
        count_l=2
        display_left('Counter-Clk')
        direction(p,"counter-clockwise")
        
def GPIO23_callback(channel):
        global count_l
        count_l=3
        display_left('stop')
        direction(p,"stop")
        
def GPIO27_callback(channel):
        global count_r
        count_r=1
        display_right('Clkwise')
        direction(p2,"clockwise")
        
def GPIO19_callback(channel):
        global count_r
        count_r=2
        display_right('Counter-Clk')
        direction(p2,"counter-clockwise")

def GPIO26_callback(channel):
        global count_r
        count_r=3
        display_right('start_flag')
        direction(p2,"stop")

GPIO.add_event_detect(17,GPIO.FALLING, callback=GPIO17_callback, bouncetime=200)
GPIO.add_event_detect(22,GPIO.FALLING, callback=GPIO22_callback, bouncetime=200)
GPIO.add_event_detect(23,GPIO.FALLING, callback=GPIO23_callback, bouncetime=200)
GPIO.add_event_detect(27,GPIO.FALLING, callback=GPIO27_callback, bouncetime=200)
GPIO.add_event_detect(19,GPIO.FALLING, callback=GPIO19_callback, bouncetime=200)
GPIO.add_event_detect(26,GPIO.FALLING, callback=GPIO26_callback, bouncetime=200)
#Calibrate the servo pwm
#set up the pwm frequency to 1 Hz
draw_flag =0

while (time.time()-start) <= 50 and flag !=1:
    #global start_flag, p, p2
    my_buttons = {'Quit':(240,220), center_button:(150,110),"Left History":(50,20),"Right History":(260,20)}
    leftPos = rightPos=timePos=timepos2=70
    
    screen.fill(BLACK) #Erase the work space
    if draw_flag == 0:
        pygame.draw.circle(screen,(255,0,0),(150,110),30)
    else:
        pygame.draw.circle(screen,(0,255,0),(150,110),30)
    
    for my_text, my_pos in my_buttons.items():
      text_surface = my_font.render(my_text, True, WHITE)
      rect = text_surface.get_rect(center=my_pos)
      screen.blit(text_surface,rect)
    for item in left_state:
        my_surface = my_font.render(item,True,WHITE)
        myrect = my_surface.get_rect(center = (40,leftPos))
        leftPos+=30
        screen.blit(my_surface,myrect)
    for item2 in right_state:
        my_surface = my_font.render(item2,True,WHITE)
        myrect = my_surface.get_rect(center = (220,rightPos))
        rightPos+=30
        screen.blit(my_surface,myrect)
    for i in range(len(time_state_left)):
        my_surface = my_font.render(time_state_left[i],True,WHITE)
        myrect = my_surface.get_rect(center = (100,timePos))
        timePos+=30
        screen.blit(my_surface,myrect)
    for j in range(len(time_state_right)):
        my_surface = my_font.render(time_state_right[j],True,WHITE)
        myrect = my_surface.get_rect(center = (290,timepos2))
        timepos2+=30
        screen.blit(my_surface,myrect)
    pygame.display.flip()
    
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        x,y = pos
        if (event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            x,y = pos

        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            if y>90 and x>130 and x<170 and y<130:
              if center_button == 'STOP':
                print "Stop button is pressed"
                #start_flag = 1
                direction(p, 'stop')
                direction(p2, 'stop')
                center_button = 'RESUME'
                draw_flag = 1
                break
              else:
                resume_flag = 0
                if count_l==1:
                    direction(p,"clockwise")
                    if count_r==1:
                        direction(p2,"clockwise")
                    if count_r==2:
                        direction(p2,"counter-clockwise")
                    if count_r==3:
                        direction(p2,"stop") 
                if count_l==2:
                    direction(p,"counter-clockwise")
                    if count_r==1:
                        direction(p2,"clockwise")
                    if count_r==2:
                        direction(p2,"counter-clockwise")
                    if count_r==3:
                        direction(p2,"stop")
                if count_l==3:
                    direction(p,"stop")
                    if count_r==1:
                        direction(p2,"clockwise")
                    if count_r==2:
                        direction(p2,"counter-clockwise")
                    if count_r==3:
                        direction(p2,"stop")
                if count_r==1:
                    direction(p2,"clockwise")
                    if count_l==1:
                        direction(p,"clockwise")
                    if count_l==2:
                        direction(p,"counter-clockwise")
                    if count_l==3:
                        direction(p,"stop")
                if count_r==2:
                    direction(p2,"counter-clockwise")
                    if count_l==1:
                        direction(p,"clockwise")
                    if count_l==2:
                        direction(p,"counter-clockwise")
                    if count_l==3:
                        direction(p,"stop")
                if count_r==3:
                    direction(p2,"stop")
                    if count_l==1:
                        direction(p,"clockwise")
                    if count_l==2:
                        direction(p,"counter-clockwise")
                    if count_l==3:
                        direction(p,"stop")
                print "Resume button is pressed"
                #start_flag = 0
                draw_flag = 0
                center_button = 'STOP'
                break
            if y>200 and x>230:
                print"Quit pressed"
                flag = 1
                break




##try:
##    print(" ")
##    print "Waiting for pressing GPIO13 button to Quit"
##    GPIO.wait_for_edge(13,GPIO.FALLING, timeout=100000)
##    flag = 1
##
##except KeyboardInterrupt:
##    GPIO.cleanup()
##    p2.stop()
##    p.stop()

GPIO.cleanup()
p.stop()
p2.stop()


