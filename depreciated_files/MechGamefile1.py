import pygame
import math
from pygame.locals import *
import random
import time
from abc import ABCMeta, abstractmethod
import planes
from planes import Plane
import planes.gui

from screen import DropZone
from titleScreen import TitleScreen
from moveScreen4 import MoveScreen
from MechEE_screen import MechEE_screen

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750


class Startbutton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)

	def clicked(self, button_name):
		self.model.currentscreen = self.model.playScreen

class SettingsButton(Button):
	def __init__(self, label, im, rect, callback,model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentscreen = self.model.settingsScreen

class titleRect(planes.Plane):
	def __init__(self, im, rect, color):
		planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
		self.image.fill(color)
		self.rect = rect
		self.color = color
		self.image = pygame.image.load(im)

class TargetZone(planes.Plane):
	def hitTarget(self,plane,coordinates):
		planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))
		plane.moving = False

class ToolStorage(planes.Plane):
	def 
		

class FalseTarget(self,TargetZone):
	if 

class TrueTarget(self,TargetZone):



class MechEEgame:
	def __init__(self):
		self.tools = []
		self.parts = []
		self.playScreen = Screen(self.tools, self.parts, self)
		self.levels = levels
		start = StartButton("start", "start.png", pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),StartButton.clicked,self)
		info = informationButton("information","i.jpg",pygmame.Rect(WINDOWWIDTH/8,5*WINDOWHEIGHT/8 + 20,3*WINDOWWIDTH/4,WINDOWHEIGHT/8)informationButton.clicked,self)
		tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)
		self.homescreen = Screen([start,settings,tutorial],[titleRect("home.png",tr,WHITE)],BLACK)
		self.settingsscreen = Screen([home,settings,tutorial],[titleRect("settings.png",tr,WHITE)],BLACK)
		self.infoscreen = Screen([home,settings, information],[titleRect("infortmation.png",tr,WHITE)],BLACK)