import pygame
from pygame.locals import* #for event MOUSE variables
import os
import time
import math
import RPi.GPIO as GPIO

os.putenv('SDL_VIDEODRIVER', 'fbcon') #Display on piTFT
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB') #Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
pygame.mouse.set_visible(False)
#pygame.mouse.set_visible(True)
size = width, height = 320, 240
WHITE = 255,255,255
BLACK = 0,0,0
screen = pygame.display.set_mode(size)

my_font = pygame.font.Font(None,20)

my_buttons = {'Quit':(270,220),'Start':(60,220),'touch at x , y':(150,100)}
screen.fill(BLACK)
for my_text, text_pos in my_buttons.items():
    text_surface = my_font.render(my_text, True, WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)
    
pygame.display.flip()
start = time.time()
flag=0

# setup for bouncing balls
size = width, height = 320, 240
speed = [1, 2]
speed2 = [-2, -1]

black = 0, 0, 0

screen = pygame.display.set_mode(size)

# load the image to the ball and get the rect
#with same height and width as images
ball = pygame.image.load("magic_ball.png")
ballrect = ball.get_rect()
#set the initial position of balls
ballrect.center = (64,64)
ball2 = pygame.image.load("ball.png")
ballrect2 = ball2.get_rect()
ballrect2.center = (200,200)
flag_collide = 0

while (time.time()-start) <= 70 and flag !=1:
    pos = pygame.mouse.get_pos()
    x,y = pos
    my_buttons = {'Quit':(270,220), 'Start':(60,220),'touch at '+str(x)+', '+str(y):(150,100)}
    screen.fill(BLACK)
    for my_text, text_pos in my_buttons.items():
        # set the text surface with its color and font on new surface
        text_surface = my_font.render(new_text, True, WHITE)
        #set the text surface with corresponding position
        rect = text_surface.get_rect(center=new_pos)
        #draw the text button on the work screen
        screen.blit(text_surface,rect)
    # display it on actual screen
    pygame.display.flip()
  
    if (not GPIO.input(27)):
        print(" ")
        print "Quit"
        break
    
    #count whether the odd number for pause
    count = 0
    #set the perameter for speed of the bouncing ball
    k=1
    #set the flag for pause the two bouncing ball
    flag_move=0
    for event in pygame.event.get():
    pos = pygame.mouse.get_pos()
        x,y = pos
        
        if (event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            x,y = pos

        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            my_buttons = {'Quit':(270,220), 'Start':(60,220),'touch at '+str(x)+', '+str(y):(150,100)}
            screen.fill(BLACK)
            for my_text, text_pos in my_buttons.items():
                # set the text surface with its color and font on new surface
                text_surface = my_font.render(new_text, True, WHITE)
                #set the text surface with corresponding position
                rect = text_surface.get_rect(center=new_pos)
                #draw the text button on the work screen
                screen.blit(text_surface,rect)
            # display it on actual screen
            pygame.display.flip()
            print "touch at coordinate: " +'('+str(x)+', '+str(y)+')'
            if x< 70 and y> 200:
                print "Start pressed"
                flag_collide = 1

            if y>200 and x>260 and flag_collide == 0:
                print"Quit pressed"
                flag = 1
                break

    while flag_collide == 1:
            if (not GPIO.input(27)):
               print(" ")
               print "Quit"
               break
            # update the sleep time controlling the speed of two balls
            sleep_time = k*0.02
                        
            time.sleep(sleep_time)
           # condition for pausing or resuming the balls
            if flag_move == 0:
                ballrect = ballrect.move(speed)
                ballrect2 = ballrect2.move(speed2)

            #calculate the distance from two centers of balls
            dx = ballrect.x - ballrect2.x
            dy = ballrect.y - ballrect2.y
            absolute = math.sqrt(dx*dx + dy*dy)
            # when hitcount is greater to 8, the program
            # will calculate two balls to avoid balls adjoining together 
            if (hitcount > 0):
                hitcount = hitcount+1
                if hitcount == 8:
                    hitcount=0
                    
            # when two balls touch to each other
            if absolute <= 128  and hitcount == 0:
                #calculate the changing velocity when two balls collide
                vx = speed[0] - speed2[0]
                vy = speed[1] - speed2[1]
                temp1 = (dx*vx+dy*vy)/absolute
                newx = (-dx/absolute)*temp1
                newy = (-dy/absolute)*temp1
                #add the changing velocity for ball 1
                speed = [newx+speed[0],newy+speed[1]]
                #subtract the changing velocity for ball 2
                speed2 = [speed2[0]-newx,speed2[1]-newy]
                hitcount = 1
        
            # bounce the ball back in x direction
            if ballrect.left < 0 or ballrect.right > width:
                speed[0] = -speed[0]
                
            # bounce the ball back in y direction
            if ballrect.top < 0 or ballrect.bottom > height:
                speed[1] = -speed[1]
                
            # bounce the ball back in x direction    
            if ballrect2.left < 0 or ballrect2.right > width:
                speed2[0] = -speed2[0]
                
            # bounce the ball back in y direction    
            if ballrect2.top < 0 or ballrect2.bottom > height:
                speed2[1] = -speed2[1]
                
            # erase the ball in prior position
            screen.fill(black)
            # draw two balls in new position
            screen.blit(ball, ballrect)
            screen.blit(ball2, ballrect2)
            my_buttons = {'Pause':(50,220),'Fast':(130,220),'Slow':(200,220),'Back':(270,220)}
           # display the buttons from my_button
            for my_text, my_pos in my_buttons.items():
                # set the text surface with its color and font on new surface
               text_surface = my_font.render(new_text, True, WHITE)
               #set the text surface with corresponding position
               rect = text_surface.get_rect(center=new_pos)
               #draw the text button on the work screen
               screen.blit(text_surface,rect)
            # display it on actual screen
            pygame.display.flip()
        
            for event in pygame.event.get():
                if (event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                    x2,y2 = pos
        
                elif(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x2,y2 = pos
                     print "touch at coordinate: " +'('+str(x2)+', '+str(y2)+')'
                    if y2>200:
                        if x2< 80:
                            print "Pause pressed"
                            count = count+1
                            # pause two balls when press the first or every other times
                            if (count%2 == 1):
                                flag_move = 1
                            else:
                            # resume two balls when press the second or even times
                                flag_move = 0
        
                        elif x2<160:
                            print "Fast pressed"
                            # block decreasing sleep time 
                            #when the sleep time is two small
                            if (sleep_time >= 0.008):
                                k = k-0.1
                            else:
                                k = 0.008
        
                        elif x2<230:
                            print "Slow pressed"
                            # block increasing sleep time
                            # when it is two slow
                            if (sleep_time <= 0.08):
                                k = k+0.1
                            else:
                                k=0.08
        
                        else:
                            print"Back pressed"
                            # reset the flag_collide to zero
                            flag_collide = 0  
                            # display start and quit buttons
                            my_buttons = {'Quit':(270,220), 'Start':(60,220)}
                            screen.fill(BLACK)
                            for my_text, text_pos in my_buttons.items():
                                # set the text surface with its color and font on new surface
                                text_surface = my_font.render(new_text, True, WHITE)
                                #set the text surface with corresponding position
                                rect = text_surface.get_rect(center=new_pos)
                                #draw the text button on the work screen
                                screen.blit(text_surface,rect)
                            # display it on actual screen
                            pygame.display.flip()
                            #quit the for loop
                            break
        
print "The time passes: ",(time.time()-start),"seconds"