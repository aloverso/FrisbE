import pygame
import planes
from collections import deque
from screen import Screen
from screen import Button
from screen import DropZone
import time
from random import randint

MOVEBUTTON_HEIGHT = 75
MOVEBUTTON_WIDTH = 50

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255,0,0)

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750
WHworkable = WINDOWHEIGHT - (3*MOVEBUTTON_HEIGHT + 15)

class Wall(planes.Plane):
    def __init__(self, name, im, rect):
        planes.Plane.__init__(self, name, rect, draggable=False, grab=False)
        self.image.fill(im)

class Money(planes.Plane):
    def __init__(self, name, value, im, rect):
        planes.Plane.__init__(self, name, rect, draggable=False, grab=False)
        self.image.fill(im)
        self.value = value
    def fill(self):
    	self.image.fill(BLACK)

megawall = Wall("megawall", WHITE, pygame.Rect(0, WINDOWHEIGHT-WHworkable, WINDOWWIDTH, 5))

w1 = Wall("w1", WHITE, pygame.Rect(WINDOWWIDTH/4, WINDOWHEIGHT - 3*WHworkable/4, 3*WINDOWWIDTH/4, 20))
w2 = Wall("w2", WHITE, pygame.Rect(0, (WINDOWHEIGHT - WHworkable/2), 3*WINDOWWIDTH/4, 20))
w3 = Wall("w3", WHITE, pygame.Rect(WINDOWWIDTH/4, WINDOWHEIGHT-WHworkable/4, 3*WINDOWWIDTH/4, 20))
level1goal = Wall("goal", RED, pygame.Rect(WINDOWWIDTH-120, WINDOWHEIGHT-WHworkable + 5, 120, (WINDOWHEIGHT-WHworkable)/2))
level1start = (WINDOWWIDTH,WINDOWHEIGHT)
level1walls = [megawall,w1,w2,w3, level1goal]
m1 = Money("m1",20,BLUE, pygame.Rect(100, WINDOWHEIGHT-100, 20, 20))
m2 = Money("m2",30,BLUE, pygame.Rect(100, WINDOWHEIGHT-300, 20, 20))
m3 = Money("m3",30,BLUE, pygame.Rect(100, WINDOWHEIGHT-500, 20, 20))
m5 = Money("m5",30,BLUE,pygame.Rect(100, WINDOWHEIGHT-400, 20, 20))
m0 = Money("m0", 0, BLACK, pygame.Rect(0,0,0,0))
level1money = [m5,m2,m3,m1, m0]
