run_test_v3.py
Today
4:09 PM

Weiran Wang uploaded an item
Text
run_test_v3.py
import pygame
from pygame.locals import* #for event MOUSE variables
import os
import time
import RPi.GPIO as GPIO
import math

os.putenv('SDL_VIDEODRIVER', 'fbcon') #Display on piTFT
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB') #Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)
#pygame.mouse.set_visible(True)

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
my_buttons = {'Quit':(240,220),'Start':(60,220), center_button:(150,110),"Left History":(50,20),"Right History":(260,20)}


GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
#Calibrate the servo pwm
#set up the pwm frequency to 1 Hz
draw_flag =0
prior_motion_p = ''
prior_motion_p2 = ''
count_f = count_b= count_s=count_l=count_r = 0

def direction(servo,dir):
    if dir == "clockwise":
        servo.ChangeFrequency(46.73)
        servo.ChangeDutyCycle(6.54)
    if dir == "counter-clockwise":
        servo.ChangeFrequency(46.3)
        servo.ChangeDutyCycle(7.41)
    if dir == "stop":
        servo.ChangeDutyCycle(0)

def display(left_s, right_s):
    left_state[2] = left_state[1]
        left_state[1]= left_state[0]
        left_state[0] = left_s
        t= "%.3g" %(time.time()-start_servo)
        time_state_left[2] = time_state_left[1]
        time_state_left[1] = time_state_left[0]
        time_state_left[0] = str(t)
        right_state[2] = right_state[1]
        right_state[1] = right_state[0]
        right_state[0] = right_s
        t1= "%.3g" %(time.time()-start_servo)
        time_state_right[2] = time_state_right[1]
        time_state_right[1] = time_state_right[0]
        time_state_right[0] = str(t1)

def forward():
    global count_left, count_time_left, count_right,count_time_right,count_f
    
    if count_f == 0:
        count_f = 1
        display('Clkwise','Counter-Clk')
       
    direction(p,"clockwise")
    direction(p2,"counter-clockwise")
    prior_motion_p = "clockwise"
    prior_motion_p2 = "counter-clockwise"
    
    
def backward():
    global count_left, count_time_left, count_right,count_time_right,count_b
    if count_b == 0:
        count_b = 1
        display('Counter-Clk','Clkwise')
        

    direction(p,"counter-clockwise")
    direction(p2,"clockwise")
    prior_motion_p = "counter-clockwise"
    prior_motion_p2 = "clockwise"
    
    

def stop():
    global count_left, count_time_left, count_right,count_time_right
        
    direction(p,"stop")
    direction(p2,"stop")
    prior_motion_p = "stop"
    prior_motion_p2 = "stop"
    
def left():
    global count_left, count_time_left, count_right,count_time_right,count_l
    if count_l == 0:
        count_l = 1
        display('Clkwise','Clkwise')
       
        
    direction(p,"clockwise")
    direction(p2,"clockwise")
    prior_motion_p = "clockwise"
    prior_motion_p2 = "clockwise"
    
def right():
    global count_left, count_time_left, count_right,count_time_right,count_r
    if count_r == 0:
        count_r = 1
        display('Counter-Clk','Counter-Clk')
        
    direction(p,"counter-clockwise")
    direction(p2,"counter-clockwise")
    prior_motion_p = "counter-clockwise"
    prior_motion_p2 = "counter-clockwise"
    
def draw_and_detect():
    global flag, start_flag, stop_flag, center_button,draw_flag,prior_motion_p,prior_motion_p2
    my_buttons = {'Quit':(240,220),'Start':(60,220), center_button:(150,110),"Left History":(50,20),"Right History":(260,20)}
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
                direction(p, 'stop')
                direction(p2, 'stop')
                center_button = 'RESUME'
                draw_flag = 1
                stop_flag = 1
                break
              else:
                resume_flag = 1
                stop_flag = 0
                #direction(p, prior_motion_p)
                #direction(p2, prior_motion_p2)
                print "Resume button is pressed"
                #start_flag = 0
                draw_flag = 0
                center_button = 'STOP'
                break
            if x> 50 and x<70 and y>210:
                start_flag = 1
            if y>200 and x>230:
                print"Quit pressed"
                flag = 1
                break
            
while (time.time()-start) <= 60 and flag !=1:
    start_flag = 0
    stop_flag = 0
    my_buttons = {'Quit':(240,220),'Start':(60,220), center_button:(150,110),"Left History":(50,20),"Right History":(260,20)}
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
                direction(p, 'stop')
                direction(p2, 'stop')
                center_button = 'RESUME'
                draw_flag = 1
                stop_flag = 1
                break
              else:
                #resume_flag = 0
                stop_flag = 0
                direction(p, prior_motion_p)
                direction(p2, prior_motion_p2)
                print "Resume button is pressed"
                #start_flag = 0
                draw_flag = 0
                center_button = 'STOP'
                break
            if x> 50 and x<70 and y>210:
                start_flag = 1
            if y>200 and x>230:
                print"Quit pressed"
                flag = 1
                break
    # 6:forward:counter
    # 5: forward:clock
    # 6: back:clock
    # 5: back:counter
    # left: 6: clock, 5: clock
    # right 6: counter, 5: count-clock
    quit_flag=0
    stop1 = 0
    resume=0
    start2 = time.time()
    count_new = 0
    count_new2 = 0
    count_new3 = 0
    while start_flag == 1 and stop_flag==0 and quit_flag==0 and time.time()-start2<120:
        
        if stop1 == 0:
            if resume == 1:
                if time.time()-resume_time< 2-(stop_time-start2):
                    forward()
  
                elif time.time()-resume_time< 4-(stop_time-start2):
                    stop()
                    if count_new ==0:
                        count_new = 1
                        display('Stop','Stop')
                        
                    
                elif time.time()-resume_time < 6-(stop_time-start2):
                    backward()
                    
                elif time.time()-resume_time< 8-(stop_time-start2):
                    left()
                elif time.time()-resume_time< 10-(stop_time-start2):
                    stop()
                    if count_new2==0:
                        count_new2 = 1
                        display('Stop','Stop')
                elif time.time()-resume_time< 12-(stop_time-start2):
                    right()
                elif time.time()-resume_time< 14-(stop_time-start2):
                    stop()
                    if count_new3==0:
                        count_new3 = 1
                        display('Stop','Stop')
                else:
                    resume = 0
                    start2 = time.time()
                    count_f = count_b = count_new = count_new2 = count_new3 =count_l = count_r=0
                    
            else:
                if time.time()-start2< 2:
                    forward()
                elif time.time()-start2 < 4:
                    stop()
                    if count_new ==0:
                        count_new = 1
                        display('Stop','Stop')
                elif time.time()-start2< 6:
                    backward()
                elif time.time()-start2< 8:
                    left()
                elif time.time()-start2< 10:
                    stop()
                    if count_new2 ==0:
                        count_new2 = 1
                        display('Stop','Stop')
                elif time.time()-start2< 12:
                    right()
                elif time.time()-start2< 14:
                    stop()
                    if count_new3 ==0:
                        count_new3 = 1
                        display('Stop','Stop')
                else:
                    start2 = time.time()
                    count_f = count_b = count_new = count_new2 = count_new3 = count_l = count_r=0
        
        
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
                    stop_time = time.time()
                    direction(p, 'stop')
                    direction(p2, 'stop')
                    stop1 = 1
                    draw_flag = 1
                    center_button = 'RESUME'
                    break
                  else:
                    
                    resume_time = time.time()
                    resume = 1
                    stop1 = 0
                    print "Resume button is pressed"
                    #start_flag = 0
                    draw_flag = 0
                    center_button = 'STOP'
                    break
                if y>200 and x>230:
                    print"Quit pressed"
                    flag = 1
                    quit_flag = 1
                    
        my_buttons = {'Quit':(240,220),'Start':(60,220), center_button:(150,110),"Left History":(50,20),"Right History":(260,20)}
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
        


GPIO.cleanup()
p.stop()
p2.stop()



