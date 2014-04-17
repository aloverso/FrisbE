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

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

class StartButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentscreen = self.model.buildscreen

class HomeButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentscreen = self.model.homescreen

class SettingsButton(Button):
	def __init__(self, label, im, rect, callback,model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentscreen = self.model.settingsscreen

class TutorialButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentscreen = self.model.tutorialscreen

class titleRect(planes.Plane):
	def __init__(self, im, rect, color):
		planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
		self.image.fill(color)
		self.rect = rect
		self.color = color
		self.image = pygame.image.load(im)

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
		start = StartButton("start","startbut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),StartButton.clicked, self)
		settings = SettingsButton("settings","setbut.png",pygame.Rect(WINDOWWIDTH/8,6*WINDOWHEIGHT/8 + 30,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),SettingsButton.clicked, self)
		tutorial = TutorialButton("tutorial","tutbut.png",pygame.Rect(WINDOWWIDTH/8,5*WINDOWHEIGHT/8 + 20,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),TutorialButton.clicked, self)
		home = HomeButton("home","homebut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),HomeButton.clicked, self)
		tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)
		self.homescreen = Screen([start,settings,tutorial],[titleRect("home.png",tr,WHITE)],BLACK)
		self.settingsscreen = Screen([home,settings,tutorial],[titleRect("settings.png",tr,WHITE)],BLACK)
		self.tutorialscreen = Screen([home,settings, tutorial],[titleRect("tut.png",tr,WHITE)],BLACK)

		self.currentscreen = self.homescreen

"""
TODO

- Why is the upgrade not landing on the robot
- How to print strings/numbers to screen (i.e. display money value)  <- need this for most games
"""