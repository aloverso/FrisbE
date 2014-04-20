import pygame
import math
from pygame.locals import *
import random
import time
from abc import ABCMeta, abstractmethod
import planes
from planes import Plane
import planes.gui
from screen import Screen
from screen import Button
from screen import DropZone

import MatSciScreen
from moveScreen4 import MoveScreen
from buildScreen1 import BuildScreen
from storeScreen1 import StoreScreen

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Robot(DropZone):
    def __init__(self, name, rect, im):
		DropZone.__init__(self, name, rect)
		self.vx = 0.0
		self.vy = 0.0
		self.width = rect.width
		self.height = rect.height
		self.level = 1
		self.money = 100
		#self.image = pygame.image.load(im)
		self.image.fill(im)
		self.upgrades = []
    
    def update(self):
        '''updates the actor's position and updates the rectangle object of the
        actor'''
        self.Xpos += self.vx
        self.Ypos += self.vy
        self.rect = pygame.Rect(self.Xpos, self.Ypos, self.width, self.height)

    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, coordinates)
       plane.moving = False
       self.money -= plane.cost
       self.upgrades.append(plane)
       plane.applyUpgrade(self)

    def move(self, xMove, yMove):
    	self.Xpos += xMove*self.width
    	self.Ypos += yMove*self.height

class Upgrade(planes.Plane):
    def __init__(self, name, rect, im, cost, draggable=True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.cost = cost
        self.image.fill(im)

    def clicked(self, button_name):
        self.image.fill((255,0,0))

    def applyUpgrade(self, robot):
    	pass

class RoboGame:
	def __init__(self):
		self.robot = Robot("robot", pygame.Rect(200,200,100,100), GREEN)
		self.buildscreen =  BuildScreen(self.robot,self)
		self.movescreen = MoveScreen(self.robot,self)
		self.storescreen = StoreScreen(self.robot, self)
		self.currentscreen = self.buildscreen

"""
TODO

- Why is the upgrade not landing on the robot
- How to print strings/numbers to screen (i.e. display money value)  <- need this for most games
"""