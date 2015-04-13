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
from screen import DropDisplay

import moveScreen3
from roboGame1 import RoboGame
from ModSimGame1 import ModSimGame
from MatSciGame import MatSciGame
from GameReal import MechEEgame



WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class RoboButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		#self.image.fill(im)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentGame = self.model.robogame
		self.model.inGame = True

class ModSimButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		#self.image.fill(im)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentGame = self.model.modsimgame
		self.model.inGame = True

class MatSciButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		#self.image.fill(im)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentGame = self.model.matscigame
		self.model.inGame = True

class MechEEButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		#self.image.fill(im)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentGame = self.model.MechEEgame
		self.model.inGame = True

class titleRect(planes.Plane):
	def __init__(self, im, rect, color):
		planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
		self.image.fill(color)
		self.rect = rect
		self.color = color
		#self.image = pygame.image.load(im)
		self.image.fill(im)

class Model:
	def __init__(self):
		robo = RoboButton("robogame", "RobotGameButton.png", pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/4, 5*WINDOWWIDTH/16, 3*WINDOWHEIGHT/8), RoboButton.clicked, self)
		modsim = ModSimButton("modsimbutton", "ModSimButton.png", pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/4, 5*WINDOWWIDTH/16, 3*WINDOWHEIGHT/8), ModSimButton.clicked, self)
		matsci = MatSciButton("matscibutton", "MatSciButton.png", pygame.Rect(WINDOWWIDTH/8, 11*WINDOWHEIGHT/16, 5*WINDOWWIDTH/16, 3*WINDOWHEIGHT/8), MatSciButton.clicked, self)
		mechee = ModSimButton("mecheebutton", "DesignGame.png", pygame.Rect(WINDOWWIDTH/2, 11*WINDOWHEIGHT/16, 5*WINDOWWIDTH/16, 3*WINDOWHEIGHT/8), ModSimButton.clicked, self)
		tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/16, 3*WINDOWWIDTH/4, 1*WINDOWHEIGHT/8)
		self.dashboardScreen = Screen([robo, modsim, matsci, mechee], [titleRect(BLUE, tr, WHITE)], BLACK)
		self.robogame = RoboGame()
		self.modsimgame = ModSimGame()
		self.matscigame = MatSciGame()
		self.currentScreen = self.dashboardScreen
		self.currentGame = None
		self.inGame = False

	def update(self):
		pass

class View:
	def __init__(self, model, screen):
		self.model = model
		self.screen = screen

	def draw(self):
		screen.remove_all()
		self.screen.image.fill(self.model.currentScreen.background)
		for actor in self.model.currentScreen.actors:
			self.screen.sub(actor)
		for button in self.model.currentScreen.buttons:
			self.screen.sub(button)


if __name__ == "__main__":
	pygame.init()
	size = (WINDOWWIDTH,WINDOWHEIGHT)
	screen = DropDisplay(size)
	screen.grab = True
	screen.image.fill(BLACK)
	model = Model()
	view = View(model,screen)
	running = True
	
	for actor in model.currentScreen.actors:
		screen.sub(actor)
	for button in model.currentScreen.buttons:
		screen.sub(button)
	while running:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
			    print("got pygame.QUIT, terminating")
			    raise SystemExit
		if model.inGame:
			model.currentGame.currentscreen.update()
			model.currentScreen = model.currentGame.currentscreen

		screen.process(events)
		model.update()
		screen.update()
		screen.render()
		
		view.draw()
		pygame.display.flip()
		time.sleep(.001)

	pygame.quit()