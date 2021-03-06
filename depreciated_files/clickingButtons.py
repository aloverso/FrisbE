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

class Robot(Actor):
    def __init__(x,y,width,height):
	Actor.__init__(self,x,y,width,height,"robot")

    
class Model:
    def __init__(self):
        self.button = Button1("the button",pygame.Rect(100,100,100,100),Button1.clicked)
	self.actors = [self.button]

    def update(self):
        for actor in self.actors:
            actor.update()
    
class View:
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        self.screen.fill(BLACK)
        for actor in self.model.actors:
             pygame.draw.rect(self.screen, WHITE, actor.rect)
        pygame.display.update()

class Button1(planes.gui.Button):

	def __init__(self, label, rect, callback):

		planes.gui.Button.__init__(self, label, rect, callback)

		self.image.fill((150, 150, 150))

	def clicked(self, button_name):
		print "clicked it woot"

	def update(self):
		pass


class MoveScreen:
    pygame.init()
    size = (WINDOWWIDTH,WINDOWHEIGHT)
    screen = pygame.display.set_mode(size)
    model = Model()
    view = View(model,screen)
    running = True

    screen = planes.Display((600, 600))
    screen.grab = True
    screen.image.fill((0, 128, 0))

    screen.sub(model.actors[0])

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
        
if __name__ == '__main__': 
    moveScreen()
    
