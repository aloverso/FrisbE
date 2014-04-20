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

#import MatSciScreen
#import moveScreen3

#import ModSimGame1


#from roboGame1 import RoboGame
import MechEE_screen


WINDOWWIDTH = 1200
WINDOWHEIGHT = 800

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)



class StartButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentScreen = self.model.gamescreen

class HomeButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentScreen = self.model.homescreen

class SettingsButton(Button):
	def __init__(self, label, im, rect, callback,model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentScreen = self.model.settingsscreen

class TutorialButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentScreen = self.model.tutorialscreen

class titleRect(planes.Plane):
	def __init__(self, im, rect, color):
		planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
		self.image.fill(color)
		self.rect = rect
		self.color = color
		self.image = pygame.image.load(im)


class Model:
	def __init__(self):
		self.start = StartButton("start","startbut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWWIDTH/8 + 10,3*WINDOWWIDTH/4,WINDOWWIDTH/8),StartButton.clicked, self)
		self.settings = SettingsButton("settings","setbut.png",pygame.Rect(WINDOWWIDTH/8,6*WINDOWWIDTH/8 + 30,3*WINDOWWIDTH/4,WINDOWWIDTH/8),SettingsButton.clicked, self)
		self.tutorial = TutorialButton("tutorial","tutbut.png",pygame.Rect(WINDOWWIDTH/8,5*WINDOWWIDTH/8 + 20,3*WINDOWWIDTH/4,WINDOWWIDTH/8),TutorialButton.clicked, self)
		self.home = HomeButton("home","homebut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWWIDTH/8 + 10,3*WINDOWWIDTH/4,WINDOWWIDTH/8),HomeButton.clicked, self)
		self.backhome = HomeButton("home", "mainmenu.png",pygame.Rect(0,0,100,100),HomeButton.clicked, self)
		tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)
		gamerect = pygame.Rect(100,100,450,450)
		self.homescreen = Screen([self.start,self.settings,self.tutorial],[titleRect("home.png",tr,WHITE)],BLACK)
		self.settingsscreen = Screen([self.home,self.settings,self.tutorial],[titleRect("settings.png",tr,WHITE)],BLACK)
		self.tutorialscreen = Screen([self.home,self.settings, self.tutorial],[titleRect("tut.png",tr,WHITE)],BLACK)

		#self.gamescreen = ModSimGame1.GameScreen()
		self.gamescreen = MechEE_screen.primaryScreen()
		#self.gamescreen = MatSciScreen.MixingScreen()

		#self.gamescreen = moveScreen3.MoveScreen()
		#self.gamescreen = RoboGame(self)
		self.screens = [self.homescreen, self.settingsscreen, self.tutorialscreen, self.gamescreen]
		self.currentScreen = self.homescreen

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
		screen.process(events)
		model.update()
		screen.update()
		screen.render()
		
		view.draw()
		pygame.display.flip()
		time.sleep(.001)

	pygame.quit()