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
WHstart = 245

class Wall(planes.Plane):
    def __init__(self, name, im, rect):
        planes.Plane.__init__(self, name, rect, draggable=False, grab=False)
        if isinstance(im, str):
        	self.image = pygame.image.load(im)
        else:
        	self.image.fill(im)

class Money(planes.Plane):
    def __init__(self, name, value, rect):
        planes.Plane.__init__(self, name, rect, draggable=False, grab=False)
        self.image = pygame.image.load("money.png")
        self.value = value
    def fill(self):
    	self.image.fill(BLACK)

class Level1:
	def __init__(self):
		megawall = Wall("megawall", "megawall.png", pygame.Rect(0, WINDOWHEIGHT-WHworkable, WINDOWWIDTH, 5))

		w1 = Wall("w1", "w0.png", pygame.Rect(300, 400, 700, 200))

		goal = Wall("goal", "goal.png", pygame.Rect(540,250, 120, (WINDOWHEIGHT-WHworkable)/2 + 3))
		start = (650, 700)
		walls = [megawall,w1, goal]
		m1 = Money("m1",20, pygame.Rect(100, WINDOWHEIGHT-100, 20, 20))
		m2 = Money("m2",30, pygame.Rect(100, WINDOWHEIGHT-450, 20, 20))
		m3 = Money("m3",30, pygame.Rect(WINDOWWIDTH-100, WINDOWHEIGHT-450, 20, 20))
		m4 = Money("m4",30, pygame.Rect(WINDOWWIDTH-100, WINDOWHEIGHT-100, 20, 20))
		money = [m4,m2,m3,m1]
		self.money = money
		self.walls = walls
		self.goal = goal
		self.start = start


class Level2:
	def __init__(self):
		megawall = Wall("megawall", "megawall.png", pygame.Rect(0, WINDOWHEIGHT-WHworkable, WINDOWWIDTH, 5))

		w1 = Wall("w1", "w2_1.png", pygame.Rect(0, 400, 250, 100))
		w2 = Wall("w2", "w2_2.png", pygame.Rect(900, 450, 100, 300))

		w3 = Wall("w3", "w2_3.png", pygame.Rect(700,250,200,50))
		w4 = Wall("w4", "w2_4.png", pygame.Rect(600,300,200,100))
		w5 = Wall("w5", "w2_4.png", pygame.Rect(500,400,200,100))
		w6 = Wall("w6", "w2_4.png", pygame.Rect(400,500,200,100))
		goal = Wall("goal", "goal.png", pygame.Rect(WINDOWWIDTH-160, WINDOWHEIGHT-123, 120, (WINDOWHEIGHT-WHworkable)/2 + 3))
		start = (58, 350)
		walls = [megawall,w1,w2,w3, w4, w5, w6, goal]
		m1 = Money("m1",20, pygame.Rect(650, WINDOWHEIGHT-200, 20, 20))
		m2 = Money("m2",30, pygame.Rect(100, WINDOWHEIGHT-230, 20, 20))
		m3 = Money("m3",30, pygame.Rect(520, WINDOWHEIGHT-480, 20, 20))
		m4 = Money("m4",30, pygame.Rect(WINDOWWIDTH-100, WINDOWHEIGHT-480, 20, 20))
		money = [m4,m2,m3,m1]
		self.money = money
		self.walls = walls
		self.goal = goal
		self.start = start

class Level3:
	def __init__(self):
		megawall = Wall("megawall", "megawall.png", pygame.Rect(0, WINDOWHEIGHT-WHworkable, WINDOWWIDTH, 5))

		w1 = Wall("w1", "wall1.png", pygame.Rect(WINDOWWIDTH/4, WINDOWHEIGHT - 3*WHworkable/4, 3*WINDOWWIDTH/4, 20))
		w2 = Wall("w2", "wall1.png", pygame.Rect(0, (WINDOWHEIGHT - WHworkable/2), 3*WINDOWWIDTH/4, 20))
		w3 = Wall("w3", "wall1.png", pygame.Rect(WINDOWWIDTH/4, WINDOWHEIGHT-WHworkable/4, 3*WINDOWWIDTH/4, 20))
		goal = Wall("goal", "goal.png", pygame.Rect(WINDOWWIDTH-120, WINDOWHEIGHT-WHworkable + 5, 120, (WINDOWHEIGHT-WHworkable)/2 + 3))
		start = (WINDOWWIDTH,WINDOWHEIGHT)
		walls = [megawall,w1,w2,w3, goal]
		m1 = Money("m1",20, pygame.Rect(100, WINDOWHEIGHT-100, 20, 20))
		m2 = Money("m2",30, pygame.Rect(100, WINDOWHEIGHT-350, 20, 20))
		m3 = Money("m3",30, pygame.Rect(400, WINDOWHEIGHT-480, 20, 20))
		m4 = Money("m4",30, pygame.Rect(WINDOWWIDTH-100, WINDOWHEIGHT-200, 20, 20))
		money = [m4,m2,m3,m1]
		self.money = money
		self.walls = walls
		self.goal = goal
		self.start = start
