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

import MatSciScreen
import moveScreen3
from roboGame1 import RoboGame
from ModSimGame1 import ModSimGame



WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class RoboButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image.fill(im)
		#self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentGame = self.model.robogame
		self.model.inGame = True

class ModSimButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image.fill(im)
		#self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentGame = self.model.modsimgame
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
		robo = RoboButton("robogame", GREEN, pygame.Rect(WINDOWWIDTH/8, 3*WINDOWHEIGHT/8, 5*WINDOWWIDTH/16, 3*WINDOWHEIGHT/8), RoboButton.clicked, self)
		modsim = ModSimButton("modsimbutton", GREEN, pygame.Rect(WINDOWWIDTH/2, 3*WINDOWHEIGHT/8, 5*WINDOWWIDTH/16, 3*WINDOWHEIGHT/8), ModSimButton.clicked, self)
		tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 1*WINDOWHEIGHT/8)
		self.dashboardScreen = Screen([robo, modsim], [titleRect(BLUE, tr, WHITE)], BLACK)
		self.robogame = RoboGame()
		self.modsimgame = ModSimGame()
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
		for button in self.model.currentScreen.buttons:
			self.screen.sub(button)
		for actor in self.model.currentScreen.actors:
			self.screen.sub(actor)

if __name__ == "__main__":
	pygame.init()
	size = (WINDOWWIDTH,WINDOWHEIGHT)
	screen = MatSciScreen.DropDisplay(size)
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