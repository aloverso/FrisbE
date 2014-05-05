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
import storeScreen1


from moveScreen4 import MoveScreen
from buildScreen1 import BuildScreen
from storeScreen1 import StoreScreen

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

scrleft = 50
scrright = 1150
scrtop = 50
scrbottom = 700

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

class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.toDash = True

class Robot(planes.Plane):
    def __init__(self, name, rect, im):
		planes.Plane.__init__(self, name, rect, draggable=False, grab = False)
		self.Xpos = rect.x
		self.Ypos = rect.y
		self.width = rect.width
		self.height = rect.height
		self.level = 1
		self.money = 100
		self.image = pygame.image.load(im)
		#self.image.fill(im)
		self.upgrades = []
		self.startX = rect.x
		self.startY = rect.y
		self.motorspeed = 0.4
		self.defaultMotorspeed = 0.4
		self.bumper = 10
		self.defaultBumper = 10
    
    def update(self):
        '''updates the actor's position and updates the rectangle object of the
        actor'''
        self.rect = pygame.Rect(self.Xpos, self.Ypos, self.width, self.height)

    def move(self, xMove, yMove):
    	self.Xpos += xMove
    	self.Ypos += yMove

    def setPosition(self,x,y):
		self.Xpos = x
		self.Ypos = y

class RoboGame:
	def __init__(self):
		self.robot = Robot("robot", pygame.Rect(400,400,58,50), "robot_head.png")
		self.purchases = []
		self.buildscreen =  BuildScreen(self.robot,self)
		self.movescreen = MoveScreen(self.robot,self)
		self.storescreen = StoreScreen(self.robot, self)

		back = BackButton("back", "back_button_long.png", pygame.Rect(50,650,500,50), BackButton.clicked, self)

		start = StartButton("start","start_button.png",pygame.Rect(650,50,500,300),StartButton.clicked, self)
		tutorial = TutorialButton("tutorial","tutorial_button.png",pygame.Rect(650, 400, 500, 300),TutorialButton.clicked, self)
		home = HomeButton("home","title_button.png",pygame.Rect(650,50,500,300),HomeButton.clicked, self)
		tr = pygame.Rect(50, 50, 500, 575)
		self.homescreen = Screen([start,tutorial, back],[titleRect("robowrangler_logo.png",tr,WHITE)],BLACK)
		self.tutorialscreen = Screen([home],[titleRect("robo_tutorial.png",tr,WHITE)],BLACK)

		self.currentscreen = self.homescreen
		self.toDash = False