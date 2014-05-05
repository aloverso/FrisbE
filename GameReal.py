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


class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.toDash = True

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
        self.tools.append(Tools("Hammer",1,pygame.Rect(50,0,100,100),"hammer.png"))
        self.tools.append(Tools("Wrench",2,pygame.Rect(50,200,100,100),"wrench.png"))
        self.parts.append(Parts("Gear",5,pygame.Rect(900,200,100,100),"gears.png"))
        self.parts.append(Parts("Nut",6,pygame.Rect(900,400,100,100),"nut.png"))
        self.parts.append(Parts("Nail",7,pygame.Rect(900,600,100,100),"nails.png"))

        self.playScreen = playScreen(self.tools, self.parts, self)
        self.infoScreen = infoScreen(self.tools,self.parts, self)
        
        start = StartButton("start","startbut.png",pygame.Rect(WINDOWWIDTH/2+100,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),StartButton.clicked, self)
        info = infoScreenButton("info","i_small.png",pygame.Rect(WINDOWWIDTH/2+100,6*WINDOWHEIGHT/8 + 30,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),infoScreenButton.clicked, self)
        back = BackButton("back", "back_button_long.png", pygame.Rect(50,650,500,50), BackButton.clicked, self)

        start = StartButton("start","start_button.png",pygame.Rect(650,50,500,300),StartButton.clicked, self)
        tutorial = TutorialButton("tutorial","tutorial_button.png",pygame.Rect(650, 400, 500, 300),TutorialButton.clicked, self)
        home = HomeButton("home","title_button.png",pygame.Rect(650,50,500,300),HomeButton.clicked, self)
        tr = pygame.Rect(50, 50, 500, 575)
        self.homescreen = Screen([start,tutorial, back],[titleRect("gearup_logo.png",tr,WHITE)],BLACK)
        self.tutorialscreen = Screen([home, tutorial],[titleRect("robo_tutorial.png",tr,WHITE)],BLACK)

        self.currentscreen = self.homescreen