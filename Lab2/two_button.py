import pygame
from pygame.locals import* #for event MOUSE variables
import os
import time
import RPi.GPIO as GPIO
import subprocess
import math

#os.putenv('SDL_VIDEODRIVER', 'fbcon') #Display on piTFT
#os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB') #Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
#pygame.mouse.set_visible(False)
pygame.mouse.set_visible(True)

size = width, height = 320, 240
WHITE = 255,255,255
BLACK = 0,0,0
screen = pygame.display.set_mode(size)

my_font = pygame.font.Font(None,20)

my_buttons = {'Quit':(240,220), 'touch at x , y':(60,30), 'Start':(60,220)}
screen.fill(BLACK) #Erase the work space

for my_text, text_pos in my_buttons.items():
	text_surface = my_font.render(my_text, True, WHITE)
	rect = text_surface.get_rect(center=text_pos)
	screen.blit(text_surface,rect)

pygame.display.flip()
start = time.time()
flag=0

size = width, height = 320, 240
speed = [1, 2]
speed2 = [-2, -1]

black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("magic_ball.png")
ballrect = ball.get_rect()
ballrect.center = (64,64)


ball2 = pygame.image.load("ball.png")
ballrect2 = ball2.get_rect()
ballrect2.center = (200,200)
flag_collide = 0

        
        

while (time.time()-start) <= 30 and flag !=1:
        
        if (not GPIO.input(27)):
            print(" ")
            print "Quit"
            break
    
      	for event in pygame.event.get():
                      
      		pos = pygame.mouse.get_pos()
      		x,y = pos
      		if (event.type is MOUSEBUTTONDOWN):
      			pos = pygame.mouse.get_pos()
      			x,y = pos
      
      		elif(event.type is MOUSEBUTTONUP):
      			pos = pygame.mouse.get_pos()
      			x,y = pos
      			screen.fill(BLACK) #Erase the work space
            my_buttons = {'Quit':(240,220), 'touch at '+str(x)+', '+str(y):(60,30), 'Start':(60,220)}
            for my_text, my_pos in my_buttons.items():
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=my_pos)
                screen.blit(text_surface,rect)
            pygame.display.flip()
			      print "touch at coordinate: " +'('+str(x)+', '+str(y)+')'
			      if x< 70 and y> 200:
               print "Start pressed"
               flag_collide = 1
                            
			      if y>200 and x>230:
	             print"Quit pressed"
               flag = 1
	             break

        if flag_collide == 1:
            

                    ballrect = ballrect.move(speed)
                    ballrect2 = ballrect2.move(speed2)
                    dx = ballrect.x - ballrect2.x
                    dy = ballrect.y - ballrect2.y
                    absolute = math.sqrt(dx*dx + dy*dy)
                    hitcount=0
            
                    if (hitcount > 0):
                        hitcount = hitcount+1
                        if hitcount == 8:
                            hitcount=0
            

                    if absolute <= 48  and hitcount == 0:
                        vx = speed[0] - speed2[0]
                        vy = speed[1] - speed2[1]
                        temp1 = (dx*vx+dy*vy)/absolute
                        newx = (-dx/absolute)*temp1
                        newy = (-dy/absolute)*temp1
                        speed = [newx+speed[0],newy+speed[1]]
                        speed2 = [speed2[0]-newx,speed2[1]-newy]
                        hitcount = 1


                    if ballrect.left < 0 or ballrect.right > width:
                        speed[0] = -speed[0]
        

                    if ballrect.top < 0 or ballrect.bottom > height:
                        speed[1] = -speed[1]
        
        
                    if ballrect2.left < 0 or ballrect2.right > width:
                        speed2[0] = -speed2[0]
                
            
                    if ballrect2.top < 0 or ballrect2.bottom > height:
                        speed2[1] = -speed2[1]
          
                    screen.fill(black)
                    screen.blit(ball, ballrect)
                    screen.blit(ball2, ballrect2)
                    new_buttons = {'Quit':(240,220), 'touch at '+str(x)+', '+str(y):(60,30),'Start':(60,220)}
                    for my_text, my_pos in my_buttons.items():
                        text_surface = my_font.render(my_text, True, WHITE)
                        rect = text_surface.get_rect(center=my_pos)
                        screen.blit(text_surface,rect)
                    pygame.display.flip()
		

print "The time passes: ",(time.time()-start),"seconds"