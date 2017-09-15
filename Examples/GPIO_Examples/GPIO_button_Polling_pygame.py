#!/usr/bin/python2.7
'''
Description: This program polls the hardware buttons on the PiTFT display and lights up the screen
             and displays the GPIO number of the button last pressed.

Created on Jul 12, 2014

@author: jeremyblythe
'''
import pygame
import os
from time import sleep
import RPi.GPIO as GPIO

# Map each switch to its own unique color. Note that the number are the BCM pin number the switches are attached to
button_map = {17:(255,0,0), 22:(0,255,0), 23:(0,0,255), 27:(0,0,0)}

#Setup the GPIOs as inputs with Pull Ups since the buttons are connected to GND
GPIO.setmode(GPIO.BCM)
for k in button_map.keys():
    GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Colours
WHITE = (255,255,255)

# Set the DISPLAY environmental variable to make sure that the GUI shows up on the PiTFT display
os.putenv('DISPLAY', ':0')

pygame.init()

# Note, this command will hide the mouse but prevents the touchscreen from working correctly
# with the pygame GUI! Only use this command if you don't need to use the touchscreen with
# your program.
pygame.mouse.set_visible(False)

lcd = pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
lcd.fill((0,0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 100)

while True:
    # Scan the buttons
    for (k,v) in button_map.items():
        if GPIO.input(k) == False:
            lcd.fill(v)
            text_surface = font_big.render('%d'%k, True, WHITE)
            rect = text_surface.get_rect(center=(160,120))
            lcd.blit(text_surface, rect)
            pygame.display.update()
    sleep(0.1)    
