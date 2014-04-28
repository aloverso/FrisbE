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

w1_1 = Wall("w1_1", WHITE, pygame.Rect(WINDOWWIDTH/4, WINDOWHEIGHT - 3*WHworkable/4, 3*WINDOWWIDTH/4, 20))
w1_2 = Wall("w1_2", WHITE, pygame.Rect(0, (WINDOWHEIGHT - WHworkable/2), 3*WINDOWWIDTH/4, 20))
w1_3 = Wall("w1_3", WHITE, pygame.Rect(WINDOWWIDTH/4, WINDOWHEIGHT-WHworkable/4, 3*WINDOWWIDTH/4, 20))
level1goal = Wall("goal", RED, pygame.Rect(WINDOWWIDTH-120, WINDOWHEIGHT-WHworkable + 5, 120, (WINDOWHEIGHT-WHworkable)/2))
level1start = (WINDOWWIDTH,WINDOWHEIGHT)
level1walls = [megawall,w1_1,w1_2,w1_3, level1goal]
m1_1 = Money("m1_1",20,BLUE, pygame.Rect(100, WINDOWHEIGHT-100, 20, 20))
m1_2 = Money("m1_2",30,BLUE, pygame.Rect(100, WINDOWHEIGHT-350, 20, 20))
m1_3 = Money("m1_3",30,BLUE, pygame.Rect(100, WINDOWHEIGHT-500, 20, 20))
m1_4 = Money("m1_4",30,BLUE,pygame.Rect(WINDOWWIDTH-100, WINDOWHEIGHT-200, 20, 20))
level1money = [m1_4,m1_2,m1_3,m1_1]
