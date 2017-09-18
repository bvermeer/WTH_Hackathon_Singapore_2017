#!/usr/bin/python2.7
import sys, pygame, os

os.putenv('DISPLAY', ':0')

pygame.init()

size = width, height = 320, 240
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# Be careful with this line! The touchscreen doesn't work correctly when hiding the mouse!
pygame.mouse.set_visible(False)

ball = pygame.image.load("./Images/ball.png")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()