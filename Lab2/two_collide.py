import pygame
import os
import time
import math
# os.putenv('SDL_VIDEODRIVE','fbcon')
# os.putenv('SDL_FBDEV','/dev/fb0')
pygame.init()

#set initial value for screen and balls' speed
size = width, height = 720, 640
speed = [1, 2]
speed2 = [2, 1]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
#set parameter for ball 1
ball = pygame.image.load("magic_ball.png")
ballrect = ball.get_rect()
ballrect.center = (64,64)

# set parameter for ball 2
ball2 = pygame.image.load("balls.png")
ballrect2 = ball2.get_rect()
ballrect2.center = (500,500)
hitcount=0

while 1:
    time.sleep(0.01)
    #move the ball with speed
    ballrect = ballrect.move(speed)
    ballrect2 = ballrect2.move(speed2)
    # get the speed difference in x and y direction
    dx = ballrect.x - ballrect2.x
    dy = ballrect.y - ballrect2.y
    absolute = math.sqrt(math.pow(dx,2)+math.pow(dy,2))
    # implement a hitcount to avoid two balls clustered together
    if (hitcount > 0):
        hitcount = hitcount+1
        if hitcount == 8:
            hitcount=0
            
    #when two ball is touch to each other
    if absolute <= 128  and hitcount == 0:
        vx = speed[0] - speed2[0]
        vy = speed[1] - speed2[1]
        temp1 = (dx*vx+dy*vy)/absolute
        newx = (-dx/absolute)*temp1
        newy = (-dy/absolute)*temp1
        #update the new speed for two balls
        speed = [newx+speed[0],newy+speed[1]]
        speed2 = [speed2[0]-newx,speed2[1]-newy]
        hitcount = 1

    # check if the ball is out of the screen
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
        

    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
        
        
    if ballrect2.left < 0 or ballrect2.right > width:
        speed2[0] = -speed2[0]
        
        
    if ballrect2.top < 0 or ballrect2.bottom > height:
        speed2[1] = -speed2[1]
        
    #erase the screen
    screen.fill(black)
    #plot two balls on the screen
    screen.blit(ball, ballrect)
    screen.blit(ball2, ballrect2)
    pygame.display.flip()
    
