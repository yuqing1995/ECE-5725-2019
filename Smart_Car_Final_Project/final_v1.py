from multiprocessing import Process, Queue, Value, Lock, Array
import numpy as np
import cv2
import time
import os
import RPi.GPIO as GPIO
import datetime


# This system command loads the right drivers for the Raspberry Pi camera
os.system('sudo modprobe bcm2835-v4l2')
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
#setup for IR sensor
GPIO.setup(26, GPIO.IN)

#set up left wheel frequency
p_left = GPIO.PWM(5, 46.5)
#set up right wheel frequency
p_right = GPIO.PWM(6, 46.5)
#set up left wheel duty cycle
p_left.start(6.977)
#set up right wheel duty cycle
p_right.start(6.977)

objectColor = []

while(1):
    color = "Enter the command: "
    user_in = raw_input(color)
    if(user_in=='start'):
        break;
    objectColor.append(user_in)
    
    
##
##for i in range(len(object)):
##    print object[i]


#set up the width and height for the pi camera window
w=480
h=320

my_camera = cv2.VideoCapture(0)
my_camera.set(3,w)
my_camera.set(4,h)
time.sleep(2)

#define global variables for motor speed 
quater_speed_counter = 7.1
half_speed_counter = 7.2
full_speed_counter = 7.9
quater_speed_clk = 6.8
half_speed_clk = 6.6
full_speed_clk = 6.04
#define global variable for current color range 

# function for motor to change direciton
def direction(servo,dir,speed):
    global quater_speed_counter, quater_speed_clk
    if speed == 'fast':    
        if dir == "clockwise":
            servo.ChangeFrequency(46.5)
            servo.ChangeDutyCycle(half_speed_clk)
        if dir == "counter-clockwise":
            servo.ChangeFrequency(46.3)
            servo.ChangeDutyCycle(half_speed_counter)
    else:
        if dir == "clockwise":
            servo.ChangeFrequency(46.5)
            servo.ChangeDutyCycle(quater_speed_clk)
        if dir == "counter-clockwise":
            servo.ChangeFrequency(46.3)
            servo.ChangeDutyCycle(quater_speed_counter)
            
    if dir == "stop":
            servo.ChangeDutyCycle(0)

def turn_right():
    direction(p_right, "counter-clockwise","slow");
    direction(p_left, "counter-clockwise", "slow");

def turn_left():
    direction(p_left, "clockwise", "slow");
    direction(p_right, "clockwise", "slow");
    
def forward():
    direction(p_left, "counter-clockwise", "slow");
    direction(p_right, "clockwise", 'slow');
    
def backward():
    direction(p_left, "clockwise", "slow");
    direction(p_right, "counter-clockwise", 'slow');

def stop():
    direction(p_left, "stop", 'slow');
    direction(p_right, "stop", 'slow');

def currentColor(cur_color, lower_color, upper_color, colorThreshold):
    #define color range for red
    lower_red = np.array([175,100,100])
    upper_red = np.array([185,200,200])
    redThreshold = 100000 # ???
    #define color range for green
    lower_green = np.array([35,150,100])
    upper_green = np.array([50,255,200])
    greenThreshold = 100000 # ???
    #define color range for blue
    lower_blue = np.array([80, 155, 100])
    upper_blue = np.array([120,210,200])
    blueThreshold = 500000 # ???
    #define color range for yellow
    lower_yellow = np.array([10,155,155])
    upper_yellow = np.array([30,255,255])
    yellowThreshold = 100000 # ???
    if cur_color == 'red':
                lower_color = lower_red
                upper_color = upper_red
                colorThreshold = redThreshold
            if cur_color == 'green':
                lower_color = lower_green
                upper_color = upper_green
                colorThreshold = greenThreshold
            if cur_color == 'yellow':
                lower_color = lower_yellow
                upper_color = upper_yellow
                colorThreshold = yellowThreshold
            if cur_color == 'blue':
                lower_color = lower_blue
                upper_color = upper_blue
                colorThreshold = yellowThreshold


def main_process(flag_run, send_que, receive_que, pStart):
    lower_color = np.array([0,0,0])
    upper_color = np.array([0,0,0])
    colorThreshold = 0
    index = 0
    while (flag_run.value):
        cur_color = objectColor[index]
        currentColor(cur_color, lower_color, upper_color, colorThreshold)
        print cur_color, colorThreshold
        if (index == len(objectColor)-1):
            flag_run.value = 0
            print "All colors are visited"
        index += 1
        startTime = time.time()
        while 1:
            #readin the value of IR sensor to see if it is close to obstacles
            sensor_left = GPIO.input(26)
            #sensor_right = GPIO.input()
            target_x=w/2
            success, image = my_camera.read()
            image = cv2.flip(image,-1)
            image = cv2.GaussianBlur(image,(5,5),0)
            image_HSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(image_HSV,lower_color,upper_color)
            # check if the blue object is detected
            sum_color = np.sum(mask)
            exceed_colorThres = sum_color>colorThreshold
            # check the start frame transaction time
            currentTime = time.time()
            diffTime = currentTime - startTime
            mask = cv2.GaussianBlur(mask,(5,5),0)
            # check if the diff time is greater than 30 seconds and then start transaction to frame
            if (diffTime > 30) and exceed_colorThres and (send_que.qsize() <= 3):
                startTime = currentTime
                send_que.put(mask)
            if (not exceed_colorThres):
                turn_right()
                print "not in the screen"
            if (not receive_que.empty()):
                lastReceiveTime = time.time()
                contours = receive_que.get()
                # If we have at least one contour, look through each one and pick the biggest
                diam = 0
                if len(contours)>0:
                    largest = 0
                    area = 0
                    for pix in range(len(contours)):
                        # get the area of the ith contour
                        temp_area = cv2.contourArea(contours[pix])
                        # if it is the biggest we have seen, keep it
                        if temp_area>area:
                            area=temp_area
                            largest = pix
                    # Compute the x coordinate of the center of the largest contour
                    coordinates = cv2.moments(contours[largest])
                    target_x = int(coordinates['m10']/coordinates['m00'])
                    target_y = int(coordinates['m01']/coordinates['m00'])
                    print '('+ target_x+','+target_y+')'
                    # Pick a suitable diameter for our target (grows with the contour)
                    diam = int(np.sqrt(area)/4)
                    if (diam > 120 and target_y < 80):
                        stop()
                        time.sleep(3)
                        print "Arrive the target color: "+ cur_color
                        backward()
                        time.sleep(3)
                        break
                    
                    else:   
                        # control motor to move toward the target
                        if (target_x < w/2-150):
                            stop()
                            #time.sleep(1)
                            turn_left()
                            print "left"
                        elif (target_x > w/2+150):
                            stop()
                            #time.sleep(1)
                            turn_right()
                            print "right"
                        else:
                            forward()
                            print "center"
                            #print target_x
                        # draw on a target
                    cv2.circle(image,(target_x,target_y),diam,(0,255,0),1)
                    cv2.line(image,(target_x-2*diam,target_y),(target_x+2*diam,target_y),(0,255,0),1)
                    cv2.line(image,(target_x,target_y-2*diam),(target_x,target_y+2*diam),(0,255,0),1)
            cv2.imshow('View',image)

                # Esc key to stop, otherwise repeat after 33 milliseconds
            key_pressed = cv2.waitKey(1)
            if key_pressed == 27:   
                flag_run = 0 
                break
    print ("main_process exit")            

def process_1(flag_run, send_que, receive_que, pStart):
    while (flag_run.value):
        startTime = time.time()
        if (not send_que.empty() and pStart.value == 1):
            mask = send_que.get()
            pStart.value = 2
            # findContours returns a list of the outlines of the white shapes in the mask (and a heirarchy that we shall ignore)            
            contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            receive_que.put(contours)
        else:
            time.sleep(0.03)
        currentTime = time.time()
    print "Process 1 exit"

def process_2(flag_run, send_que, receive_que, pStart):
    while (flag_run.value):
        startTime = time.time()
        if (not send_que.empty() and pStart.value == 2):
            mask = send_que.get()
            pStart.value = 3
            # findContours returns a list of the outlines of the white shapes in the mask (and a heirarchy that we shall ignore)            
            contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            receive_que.put(contours)
        else:
            time.sleep(0.03)
        currentTime = time.time()
    print "Process 2 exit"

def process_3(flag_run, send_que, receive_que, pStart):
    while (flag_run.value):
        startTime = time.time()
        if (not send_que.empty() and pStart.value == 3):
            mask = send_que.get()
            pStart.value = 1
            # findContours returns a list of the outlines of the white shapes in the mask (and a heirarchy that we shall ignore)            
            contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            receive_que.put(contours)
        else:
            time.sleep(0.03)
        currentTime = time.time()
    print "Process 3 exit"



if __name__ == '__main__':
    flag_run = Value('a', 1)
    pStart = Value('a', 1)
    send_que = Queue()
    receive_que = Queue()
    p0 = Process(target=main_process, args =(flag_run, send_que, receive_que, pStart))
    p1 = Process(target=process_1, args =(flag_run, send_que, receive_que, pStart))
    p2 = Process(target=process_2, args =(flag_run, send_que, receive_que, pStart))
    p3 = Process(target=process_3, args =(flag_run, send_que, receive_que, pStart))
    
    p0.start()
    p1.start()
    p2.start()
    p3.start()

    p0.join()
    p1.join()
    p2.join()
    p3.join()

    p_left.stop()
    p_right.stop()
    GPIO.cleanup()

    cv2.destroyAllWindows()
    my_camera.release()
    # due to a bug in openCV you need to call wantKey three times to get the
    # window to dissappear properly. Each wait only last 10 milliseconds
    cv2.waitKey(10)
    time.sleep(0.1)
    cv2.waitKey(10)
    cv2.waitKey(10)



