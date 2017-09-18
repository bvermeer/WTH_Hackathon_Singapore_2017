#!/usr/bin/python2.7
'''
Description: This is a simple PyGame program which starts up a fullscreen PyGame app,
             lights up the screen red for a second, and then exits.

Created on September 13, 2017

@author: Blake Vermeer 
'''
import pygame
import os
from time import sleep

# This line is needed to make sure the program is displayed on the Raspberry Pi's screen 
# when starting the program over SSH. This command should come before initializing PyGame.
os.putenv('DISPLAY', ':0')

pygame.init()

lcd = pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
lcd.fill((255,0,0))
pygame.display.update()
sleep(1)

lcd.fill((0,0,0))
pygame.display.update()