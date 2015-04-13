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


WINDOWWIDTH = 600
WINDOWHEIGHT = 600

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Actor(planes.Plane):
    def __init__(self, x, y, width, height, name="Actor", draggable=False, grab=False):
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

class Model:
    def __init__(self):
        print 'yo'
        self.button = Button1("text", pygame.Rect(100,100,100,100), clicked, background_color=None, text_color=(0, 0, 0))
        self.actors = [self.button]

    def buttonClicked(self):
	print "clicked this shit"

    def update(self):
        print 'y'
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

class Button1(planes.Button):

	def __init__(self, label, rect, callback, background_color=None, text_color=(0, 0, 0)):

		planes.Button.__init__(self, label, rect, callback, background_color=None, text_color=(0, 0, 0))

	def clicked(self, button_name):
		print "clicked"

	def update(self):
		pass

class Controller:
    def __init__(self, model):
        self.model = model
        
    def handleEvent(self, event):
         if event.type == pygame.MOUSEBUTTONUP:
            location = pygame.mouse.get_pos
            for clickable in self.model.clickables:
                if clickable.rect.collidepoint(location):
                    clickable.onClick()

if __name__ == '__main__':
    print 'aj'
    pygame.init()
    size = (WINDOWWIDTH,WINDOWHEIGHT)
    screen = pygame.display.set_mode(size)
    print 'hey'
    model = Model()
    view = View(model,screen)
    controller = Controller(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handleEvent(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
        
    
    
