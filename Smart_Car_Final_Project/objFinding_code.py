# Qing Yu (qy95), Wangwei Ran (ww463)
# ECE 5725 Final Project: Object Finding Robot
# 12/5/2018

# Basic Description
# objFinding_code.py detect different objects by colors, 
# after locating the target object, the robot navigates to the target object
# when the robot is close to object, the robot will stop and backward meaning
# that the robot finished finding current object and start to find next.
# two IR sensors on the left and right sides of the robot help the robot to avoid obstacles. 
 
# GUI User explaination
# User pressed the colors buttons want to find serialsly on the PiTFT
# Then pressed start button to let the robot start finding selected-color object
# Press Quit button to quit the program.

# import libraries
import os
import time
# This system command loads the right drivers for the Raspberry Pi camera
os.system('sudo modprobe bcm2835-v4l2')
#enable the touch screen on PiTFT
os.system('sudo rmmod stmpe_ts')
os.system('sudo modprobe stmpe_ts')
time.sleep(0.1)
import numpy as np
import cv2
import pigpio
import RPi.GPIO as GPIO
import pygame
from pygame.locals import*

# load the program to PiTFT and enable the mouse
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1') 
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()

#display the mouse on the PiTFT touch screen
pygame.mouse.set_visible(True)

#set up the GPIO 
GPIO.setmode(GPIO.BCM)
#setup for IR sensor
GPIO.setup(26, GPIO.IN)
GPIO.setup(19,GPIO.IN)
GPIO.setup(16,GPIO.IN)
# set up a bail out button to bail out from the PiTFT
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#set up hardware PWM
pi_hw = pigpio.pi()
pi_hw.hardware_PWM(12, 46.3, 69700)
pi_hw.hardware_PWM(13, 46.3, 69700)

# define the array for saving different color object 
objectColor = []

#set up the width and height for the pi camera window
w=480
h=320
center = w/2

# enable and set up the camera
my_camera = cv2.VideoCapture(0)
my_camera.set(3,w)
my_camera.set(4,h)
time.sleep(2)

#define global variables for servo speed 
quater_speed_counter = 71000.0
half_speed_counter = 72000.0
full_speed_counter = 79000.0
quater_speed_clk = 68000.0
half_speed_clk = 66000.0
full_speed_clk = 60400.0

#define global variable for storing current color range
lower_color = np.array([0,0,0])
upper_color = np.array([0,0,0])

#define the variable for servo calibration
currMovement_left = 69700.0
currMovement_right = 69700.0

#define the global variable for left and right direction
#set them to '' at first
leftDir=''
rightDir=''

# define two value to record the target object's coordinates
target_x=0
target_y=0

# define variables for GUI Pygame display
size = width,height = 320,240
white = 255,255,255
global screen
global main_font
screen = pygame.display.set_mode(size)
main_font = pygame.font.Font(None,35)

finish = 1 # flag variable used to control the main while loop
finishType = 1 # flag indicating whether the user finished selecting colors
index = 0 # indicate the which color object is currently looking for
count=0 # indicate whether it is the first time in the loop



# function for servo to change direciton based on selected speed
def direction(servo,dir):
    global quater_speed_counter, quater_speed_clk
    if servo == 'p_left':
        if dir == "clockwise":
            pi_hw.hardware_PWM(12, 46.5, quater_speed_clk)
        elif dir=="counter-clockwise":
            pi_hw.hardware_PWM(12, 46.3, quater_speed_counter)
        else:
            pi_hw.hardware_PWM(12, 0, 0)
    else:
        if dir == "clockwise":
            pi_hw.hardware_PWM(13, 46.5, quater_speed_clk)
        elif dir=="counter-clockwise":
            pi_hw.hardware_PWM(13, 46.3, quater_speed_counter)
        else:
            pi_hw.hardware_PWM(13, 0, 0)
    
# function to let the robot turn right
def turn_right():
    direction('p_right', "counter-clockwise")
    direction('p_left', "counter-clockwise")
# function to let the robot turn left
def turn_left():
    direction('p_left', "clockwise")
    direction('p_right', "clockwise")
# function to let the robot move forward    
def forward():
    direction('p_left', "counter-clockwise")
    direction('p_right', "clockwise")
# function to let the robot move backward    
def backward():
    direction('p_left', "clockwise")
    direction('p_right', "counter-clockwise")
# function to let the robot stop
def stop():
    direction('p_left', "stop")
    direction('p_right', "stop")
    
    
# PID control value using with move_control function
# The function is used for doing the movement adjustment
def move_control(leftDir,rightDir,strength):
    global currMovement_left,currMovement_right, quater_speed_counter, quater_speed_clk
    # Calculate the value for the speed increment each time 
    increment = (quater_speed_counter-quater_speed_clk)/100.0
    # if the left wheel should do clockwise motion
    if leftDir == 'clockwise':
        #calculate the current Movement value for left wheel
        currMovement_left = currMovement_left-strength*increment
        # set the current movement value to the smallest value it could be 
        #if it is smaller than the largest duty cycle
        if (currMovement_left<quater_speed_clk):
            currMovement_left = quater_speed_clk
    # if the left wheel should do counter clockwise motion
    elif leftDir == 'counter-clockwise':
        #calculate the current Movement value for left wheel
        currMovement_left = currMovement_left+strength*increment
        # set the current movement value to the largest value it could be 
        #if it is bigger than the largest duty cycle
        if (currMovement_left>quater_speed_counter):
            currMovement_left = quater_speed_counter
    # if the right wheel should do clockwise motion    
    if rightDir == 'clockwise':
        #calculate the current movement value for right wheel
        currMovement_right = currMovement_right-strength*increment
        # set the current movement value to the smallest value it could be 
        #if it is smaller than the largest duty cycle
        if (currMovement_right<quater_speed_clk):
            currMovement_right = quater_speed_clk
    # if the right wheel should do counter clockwise motion    
    elif rightDir == 'counter-clockwise':
        #calculate the current movement value for right wheel
        currMovement_right = currMovement_right+strength*increment
        # set the current movement value to the largest value it could be 
        #if it is lagger than the largest duty cycle
        if (currMovement_right>quater_speed_counter):
            currMovement_right = quater_speed_counter
    # update the new value to Hardware PWM and change the servos speed        
    pi_hw.hardware_PWM(12, 46.3, currMovement_left)
    pi_hw.hardware_PWM(13, 46.3, currMovement_right)
    #print currMovement_left, currMovement_right, strength
    
        
    
# function used to define different colors' lower and upper thredshold
# update the global variable lower_color and upper_color to the current color value 
def currentColor(cur_color):
    global lower_color, upper_color
    #define color range for red
    lower_red = np.array([160,55,55])
    upper_red = np.array([190,255,255])
    #define color range for green
    lower_green = np.array([30,55,55])
    upper_green = np.array([80,255,255])
    #define color range for blue
    lower_blue = np.array([80, 55, 55])
    upper_blue = np.array([120,255,255])
    #define color range for yellow
    lower_yellow = np.array([10,100,100])
    upper_yellow = np.array([40,255,255])
    # update the global variable lower_color 
    # and upper_color to the current color value 
    if cur_color == 'red':
        lower_color = lower_red
        upper_color = upper_red
    if cur_color == 'green':
        lower_color = lower_green
        upper_color = upper_green
    if cur_color == 'yellow':
        lower_color = lower_yellow
        upper_color = upper_yellow
    if cur_color == 'blue':
        lower_color = lower_blue
        upper_color = upper_blue  

# function to display Pygame on the PiTFT screen        
def GUI(circle_pos):
    #define different color variable
    black = 0,0,0
    red = 255,0,0
    green = 0,255,0
    yellow = 255,255,0
    blue = 0,0,255
    # fill the screen black
    screen.fill(black)
    # write the red button
    red_text = main_font.render('Red', True, red)
    red_rect = red_text.get_rect(center = (200,60))
    screen.blit(red_text,red_rect)
    # write the yellow button
    yellow_text = main_font.render('Yellow', True, yellow)
    yellow_rect = yellow_text.get_rect(center = (200,100))
    screen.blit(yellow_text,yellow_rect)
    # write the blue button
    blue_text = main_font.render('Blue', True, blue)
    blue_rect = blue_text.get_rect(center = (200,140))
    screen.blit(blue_text,blue_rect)
    # write the green button
    green_text = main_font.render('Green', True, green)
    green_rect = green_text.get_rect(center = (200,180))
    screen.blit(green_text,green_rect)
    # write the circle indicator
    circle_rect = pygame.draw.circle(screen, green, circle_pos, 10)
    # write the start button
    start_text = main_font.render('Start', True, white)
    start_rect = start_text.get_rect(center = (40,40))
    screen.blit(start_text,start_rect)
    # write the quit button
    quit_text = main_font.render('Quit', True, white)
    quit_rect = quit_text.get_rect(center = (40,220))
    screen.blit(quit_text,quit_rect)
    # display the screen on the real screen 
    pygame.display.flip()
    
# function used to avoid the right obstacles   
def avoid_right():
    print "avoid right"
    stop()
    time.sleep(1)
    backward()
    time.sleep(1)
    turn_left()
    time.sleep(1)
    forward()
    time.sleep(5)
# function used to avoid the left obstacles 
def avoid_left():
    stop()
    time.sleep(1)
    backward()
    time.sleep(1)
    turn_right()
    time.sleep(1)
    forward()
    time.sleep(5)

# The first stage of the prgram is to detect the touch screen inputs
while finish:
    time.sleep(0.1)
    # bail out function 
    #(use GPIO 27 as the button to quit the program if sth goes bad)
    if (not GPIO.input(27)):
        print(" ")
        print "Quit (bail out)"
        break
    # display the initial GUI
    if count == 0:
        GUI([120,30])
        count=1
    # detecting whether the touch screen has been energized
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        x,y = pos
        if (event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            x,y = pos
        # the touchscreen is pressed
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            # append the string of different colors in the objectColor array
            # if relative color button is pressed
            if y>50 and y< 80 and x>170:
                #print ("red")
                objectColor.append('red')
            if y> 90 and y<120 and x>170:
                #print ("yellow")
                objectColor.append('yellow')
            if y>130 and y<160 and x>170:
                #print ("blue")
                objectColor.append('blue')
            if y>170 and y<200 and x>170:
                #print ("green")
                objectColor.append('green')
            # quit the program when the user pressed quit
            if y>200 and x<100:
                #print ("quit")
                finish=0
                break
            # start the robot when the user pressed start
            if y<50 and x<60: #start
                finishType = 0
                #print ("start")

    # The second stage of program is to loop through the objectColor array until the last color
    while (index<len(objectColor) and not finishType):
        # Set up local variable x_diff, prevX_diff, and Integral_x
        x_diff = 0
        prevX_diff = 0
        Integral_x = 0
        start_time = 0
        # bail out function 
        #(use GPIO 27 as the button to quit the program if sth goes bad)
        if (not GPIO.input(27)):
            print(" ")
            print "Quit (bail out)"
            break
        # store the current looking color in cur_color
        cur_color = objectColor[index]
        # call the function to get the corresponding color lower and upper bond
        currentColor(cur_color)
        #print cur_color
        # display and move the white dot to the corresponding color button 
        if cur_color == 'red':
            GUI([120,60])
        elif cur_color == 'blue':
            GUI([120,140])
        elif cur_color == 'green':
            GUI([120,180])
        else:
            GUI([120,100])
        # increment the looping index
        index+=1

        # The third stage of program is to detect object and navigate to the object  
        while 1:
            # bail out function 
            #(use GPIO 27 as the button to quit the program if sth goes bad)
            if (not GPIO.input(27)):
                print(" ")
                print "Quit (bail out)"
                break
            #readin the value of IR sensor to see if it is close to obstacles
            sensor_center = GPIO.input(26)
            sensor_left = GPIO.input(19)
            sensor_right = GPIO.input(16)
            # call avoid_left function when left sensor energized
            if sensor_left==0:
                avoid_left()
                print "IR_left"
            # call avoid_right function when right sensor energized  
            elif sensor_right==0:
                avoid_right()
                print "IR_right"
            # read the image from camera
            success, image = my_camera.read()
            # flip the image if it is upside down
            image = cv2.flip(image,-1)
            image = cv2.GaussianBlur(image,(5,5),0)
            # change the image from BGR to HSV
            image_HSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
            # set the mask with selected color's lower and upper bond range
            mask = cv2.inRange(image_HSV,lower_color,upper_color)
            mask = cv2.GaussianBlur(mask,(5,5),0)
            # findContours returns a list of the outlines of the white shapes in the mask (and a heirarchy that we shall ignore)            
            contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            # If we have at least one contour, look through each one and pick the biggest
            diam = 0
            if len(contours)>0:
                largest = 0
                area = 0
                for i in range(len(contours)):
                    # get the area of the ith contour
                    temp_area = cv2.contourArea(contours[i])
                    # if it is the biggest we have seen, keep it
                    if temp_area>area:
                        area=temp_area
                        largest = i
                # Compute the x coordinate of the center of the largest contour
                coordinates = cv2.moments(contours[largest])
                target_x = int(coordinates['m10']/coordinates['m00'])
                target_y = int(coordinates['m01']/coordinates['m00'])
                # Pick a suitable diameter for our target (grows with the contour)
                diam = int(np.sqrt(area)/4)
                # draw on a target
                cv2.circle(image,(target_x,target_y),diam,(0,255,0),1)
                cv2.line(image,(target_x-2*diam,target_y),(target_x+2*diam,target_y),(0,255,0),1)
                cv2.line(image,(target_x,target_y-2*diam),(target_x,target_y+2*diam),(0,255,0),1)

            # show the image 
            # cv2.imshow('View',image)

            # when the robot is close to the target
            # the robot will stop and backword for 1 second
            if (diam > 60 and target_y < 240):
                stop()
                time.sleep(2)
                #print "close to object: stop"
                backward()
                time.sleep(1)
                #print "close to object: back"
                stop()
                time.sleep(1)
                #print "close to object: stop"
                break
                
            else:   
                # control motor to move and check the target
                # if the target is found
                if (diam>3):
                    # calculate the error difference between the target_x and center
                    x_diff = abs(target_x-center)
                    #print x_diff
                    # define PID coefficiencies
                    kp = 2
                    kd = 0.005
                    ki = 0.1
                    # calculate the proportional, Derivative, and Integral Control
                    Propor_x = x_diff/(w/2.0)
                    Deriv_x = (prevX_diff - x_diff)/(time.time() - start_time)
                    Integral_x += x_diff
                    # update the start time
                    start_time = time.time()
                    # reset the integral value if it is too big or too small
                    if Integral_x<0:
                      Intrgral_x = 0
                    elif Integral_x>1000:
                      Integral_x = 1000
                    # calculate the final strength for PID control
                    strength = Propor_x*kp + Deriv_x*kd + Integral_x*ki
                    
                    # Conditions when the target is on the left of the robot
                    if (target_x < w/2-100):
                        leftDir = "clockwise"
                        rightDir = "clockwise"
                        move_control(leftDir,rightDir,strength)
                        #print "left"
                    # Conditions when the target is on the right of the robot
                    elif (target_x > w/2+100):
                        leftDir = "counter-clockwise"
                        rightDir = "counter-clockwise"
                        move_control(leftDir,rightDir,strength)
                        #print "right"
                    # Conditions when the target is in the center range
                    else:
                        forward()
                        #print "center"

                # turn left to circle around to find the target color
                else:
                    pi_hw.hardware_PWM(13, 46.5, 70500)
                    #print "not in the screen"
                
                # update the prevX_diff value    
                prevX_diff = x_diff
            # Esc key to stop, otherwise repeat after 33 milliseconds
            #key_pressed = cv2.waitKey(1)
            #if key_pressed == 27:    
            #   break

# clean up the GPIO and Hardware PWM and release the camera
GPIO.cleanup()
stop()
pi_hw.stop()
cv2.destroyAllWindows()
my_camera.release()
#time.sleep(0.1)
#cv2.waitKey(10)
#cv2.waitKey(10)




