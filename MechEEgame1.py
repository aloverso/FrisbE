mport pygame
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
from titleScreen import TitleScreen
from moveScreen4 import MoveScreen
from MechEE_screen import MechEE_screen

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

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
	




class tools(self,planes.Plane, draggable = True, grab = True):
	def __init__(self):
		self.tools.image = tools.image

class BuildScreen(Screen):
	def __init__(self,tools,parts,game):
		self.game = game

		start = StartButton("movescreen", pygame.Rect(WINDOWHEIGHT -50, 75, 50))

		Screen.__init__(self,buttons,self.actors,BLACK)

		if model.inGame:
			model.currentGame.currentscreen.update()
			model.currentScreen = model.currentGame.currentScreen

	def update(self):
		for actor in self.actors:
			actor.update

		if model.inGame:

			model.currentGame.currentscreen.update()
			model.currentScreen = model.currentGame.currentScreen

class StartButton(Button):
	def __init__(self, label, im, rect, callback, model):

		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, nutton_name):
		self.model.currentscreen = self.model.buildscreen