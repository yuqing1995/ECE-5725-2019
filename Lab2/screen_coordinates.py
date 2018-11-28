import pygame
from pygame.locals import* #for event MOUSE variables
import os
import time
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

size = width, height = 320, 240 #set up screen size
WHITE = 255,255,255 #define color variables
BLACK = 0,0,0
screen = pygame.display.set_mode(size)

my_font = pygame.font.Font(None,30)

# set a dictionary for my_buttons
# to store the button information
# with button text and the button position 
my_buttons = {'Quit':(240,220), 'touch at x , y':(150,100)}
screen.fill(BLACK) #Erase the work space

for my_text, text_pos in my_buttons.items():
    text_surface = my_font.render(my_text, True, WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)

pygame.display.flip()
start = time.time()
flag=0


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
        new_buttons = {'Quit':(240,220), 'touch at '+str(x)+', '+str(y):(150,100)}
         # display the buttons from my_button
        for new_text, new_pos in new_buttons.items():
            # set the text surface with its color and font on new surface
            text_surface = my_font.render(new_text, True, WHITE)
            #set the text surface with corresponding position
            rect = text_surface.get_rect(center=new_pos)
            #draw the text button on the work screen
            screen.blit(text_surface,rect)
        # display it on actual screen
        pygame.display.flip()
            print "touch at coordinate: " +'('+str(x)+', '+str(y)+')'
            if y>200 and x>230:
                print"Quit pressed"
                flag = 1
                break
print "The time passes: ",(time.time()-start),"seconds"
