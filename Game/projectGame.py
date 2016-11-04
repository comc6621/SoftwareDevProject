import pygame, sys
from pygame.locals import *
from sys import exit

#global vars
WHITE = (255,255,255)
GREEN = (0, 255, 0)
FPS = 30
pygame.init()
fpsClock = pygame.tick.Clock()
charSprite = pygame.image.load('waluigi.png')

#quits program if appropriate
def quitter():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            pygame.quit()
            exit()
    return

#actual gameplay
def gameplay(DISPLAYSURF):
    DISPLAYSURF.fill(GREEN)
    dead = False
    charX = 100
    charY = 450
    while not dead:
        DISPLAYSURF.fill(GREEN)
        DISPLAYSURF.blit(charSprite,charX,charY)
        if(charX < 700):
            charX = charX + 1
        else:
            dead = True
        quitter()
        pygame.display.update()
        fpsClock.tick(FPS)
    return

#start screen
def startWindow(DISPLAYSURF):
    return

DISPLAYSURF=pygame.display.set_mode((800,600))
pygame.display.set_caption('The Game^tm')
gameplay(DISPLAYSURF)
