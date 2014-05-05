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

from playScreen import playScreen
from infoScreen import infoScreen

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
		self.model.currentscreen = self.model.playScreen

class HomeButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentscreen = self.model.homescreen


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

class Tools(planes.Plane):
    def __init__(self, name, number, rect, im, draggable = True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.position = rect.center
        self.Xpos = self.position[0]
        self.Ypos = self.position[1]
        self.name = name
        self.number = number
        if isinstance(im, str):
            self.image = pygame.image.load(im)
        else:
            self.image.fill(im)
    

class Parts(planes.Plane):
    def __init__(self, name, number, rect, im, draggable = True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.position = rect.center
        self.Xpos = self.position[0]
        self.Ypos = self.position[1]
        self.name = name
        self.number = number
        if isinstance(im, str):
            self.image = pygame.image.load(im)
        else:
            self.image.fill(im)
	
        
class MechEEgame():
    def __init__(self):
        self.tools = []
        self.parts = []
        self.targets = []
        self.level = 0
        self.actors = self.tools + self.parts

        self.toDash = False
        self.tools.append(Tools("Hammer",1,pygame.Rect(500,0,20,20),WHITE))
        self.tools.append(Tools("Wrench",2,pygame.Rect(500,1*WINDOWHEIGHT/5,20,20),BLUE))
        self.parts.append(Parts("Gear",5,pygame.Rect(50,0,20,20),GREEN))
        self.parts.append(Parts("Nut",6,pygame.Rect(50,WINDOWHEIGHT/5,20,20),WHITE))
        self.parts.append(Parts("Nail",7,pygame.Rect(50,2*WINDOWHEIGHT/5,20,20),BLUE))

        self.playScreen = playScreen(self.tools, self.parts, self)
        self.infoScreen = infoScreen(self.tools,self.parts, self)
        
        start = StartButton("start","startbut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),StartButton.clicked, self)
        info = infoScreenButton("info","i.jpg",pygame.Rect(WINDOWWIDTH/8,6*WINDOWHEIGHT/8 + 30,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),infoScreenButton.clicked, self)
        tutorial = TutorialButton("tutorial","tutbut.png",pygame.Rect(WINDOWWIDTH/8,5*WINDOWHEIGHT/8 + 20,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),TutorialButton.clicked, self)
        home = HomeButton("home","homebut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),HomeButton.clicked, self)
        tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)

        self.homescreen = Screen([start,tutorial],[titleRect("home.png",tr,WHITE)],BLACK)
    
        self.currentscreen = self.homescreen