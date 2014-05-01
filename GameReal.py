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
		self.model.currentscreen = self.model.startScreen

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

class PlayScreenButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.playScreen

class infoScreenButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.infoScreen
        
class titleRect(planes.Plane):
	def __init__(self, im, rect, color):
		planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
		self.image.fill(color)
		self.rect = rect
		self.color = color
		self.image = pygame.image.load(im)

#Stuff I need for my game: Tools, Parts, Target Location

class Tool(planes.Plane):
    def __init__(self, name, number, rect, draggable = True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.image.fill((255, 0, 0))

        self.position = rect.center
        self.Xpos = self.position[0]
        self.Ypos = self.position[1]
        self.name = name
        self.number = number
    
    def clicked(self, button_name):
        self.image.fill((255,0,0))

class Parts(planes.Plane):
	def __init__(self, name, number, rect, draggable = True, grab = True):
		self.position = rect.right
		self.Xpos = self.position[0]
		self.Ypos = self.position[1]
		self.name = name
		self.number = number

	def clicked(self, button_name):
		pass



class Target(planes.Plane):
	def __init__(self, name, number, rect, draggable = False, grab = False):
		self.position = rect.center
		self.Xpos = self.position[0]
		self.Ypos = self.position[1]
		self.name = name
		self.number = number

	
        
class MechEEgame():
    def __init__(self):
        self.tools = []
        self.parts = []
        self.targets = []
        self.level = 0
        self.actors = self.tools + self.targets + self.parts
        
        self.startScreen = playScreen(self, self.tools, self.parts)
        self.infoScreen = infoScreen(self, self.tools, self.parts)
        
        start = StartButton("start","startbut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),StartButton.clicked, self)
        settings = SettingsButton("settings","setbut.png",pygame.Rect(WINDOWWIDTH/8,6*WINDOWHEIGHT/8 + 30,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),SettingsButton.clicked, self)
        tutorial = TutorialButton("tutorial","tutbut.png",pygame.Rect(WINDOWWIDTH/8,5*WINDOWHEIGHT/8 + 20,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),TutorialButton.clicked, self)
        home = HomeButton("home","homebut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),HomeButton.clicked, self)
        tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)
        self.homescreen = Screen([start,settings,tutorial],[titleRect("home.png",tr,WHITE)],BLACK)
        self.settingsscreen = Screen([home,settings,tutorial],[titleRect("settings.png",tr,WHITE)],BLACK)
        self.tutorialscreen = Screen([home,settings, tutorial],[titleRect("tut.png",tr,WHITE)],BLACK)
    
        self.currentscreen = self.homescreen