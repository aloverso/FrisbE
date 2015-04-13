# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 18:49:26 2014

@author: anneubuntu
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 00:32:11 2014

@author: anneubuntu
"""

import pygame
import math
from pygame.locals import *
import random
import time
from abc import ABCMeta, abstractmethod
import planes
from planes import Plane
import planes.gui

WINDOWWIDTH = 600
WINDOWHEIGHT = 600

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)



class Actor(planes.Plane):
    def __init__(self, x, y, width, height, name, draggable=False, grab=False):
	planes.Plane.__init__(self, name, pygame.Rect(x,y,width,height), draggable, grab)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vx = 0.0
        self.vy = 0.0
    
    def update(self):
        '''updates the actor's position and updates the rectangle object of the
        actor'''
        self.x += self.vx
        self.y += self.vy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
class MainModel:
    def __init__(self):
        self.startbutton = StartButton("start",pygame.Rect(WINDOWWIDTH/8,4*WINDOWWIDTH/8 + 10,3*WINDOWWIDTH/4,WINDOWWIDTH/8),StartButton.clicked)
	self.tutorialbutton = TutorialButton("tutorial",pygame.Rect(WINDOWWIDTH/8,5*WINDOWWIDTH/8 + 20,3*WINDOWWIDTH/4,WINDOWWIDTH/8),TutorialButton.clicked)
	self.settingsbutton = SettingsButton("settings",pygame.Rect(WINDOWWIDTH/8,6*WINDOWWIDTH/8 + 30,3*WINDOWWIDTH/4,WINDOWWIDTH/8),SettingsButton.clicked)
	self.title = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)
	self.actors = [self.startbutton, self.tutorialbutton, self.settingsbutton]

    def update(self):
        for actor in self.actors:
            actor.update()

    
class MainView:
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        self.screen.fill(BLACK)
        for actor in self.model.actors:
             pygame.draw.rect(self.screen, WHITE, actor.rect)
	pygame.draw.rect(self.screen, BLUE, self.model.title)
        pygame.display.update()

class Button(planes.gui.Button):

	def __init__(self, label, rect, callback):

		planes.gui.Button.__init__(self, label, rect, callback)

		self.image.fill((150, 150, 150))

	

	def update(self):
		pass

class StartButton(Button):
	def __init__(self, label, rect, callback):

		Button.__init__(self, label, rect, callback)

	def clicked(self, button_name):
		print "go to start screen"
class SettingsButton(Button):
	def __init__(self, label, rect, callback):

		Button.__init__(self, label, rect, callback)

	def clicked(self, button_name):
		print "settings"
class TutorialButton(Button):
	def __init__(self, label, rect, callback):

		Button.__init__(self, label, rect, callback)

	def clicked(self, button_name):
		print "go to tutorial screen"


class MainScreen:
    print "main screen muthafuckerzzzzzzzz"
    pygame.init()
    size = (WINDOWWIDTH,WINDOWHEIGHT)
    screen = pygame.display.set_mode(size)
    model = MainModel()
    view = MainView(model,screen)
    running = True

    screen = planes.Display((600, 600))
    screen.grab = True
    screen.image.fill((0, 128, 0))

    for actor in model.actors:
	screen.sub(actor)

    while running:

        events = pygame.event.get()

	for event in events:

		if event.type == pygame.QUIT:
		    print("got pygame.QUIT, terminating")
		    raise SystemExit

	screen.process(events)
	screen.update()
	screen.render()
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
        
#if __name__ == '__main__': 
#    MainScreen()
    
