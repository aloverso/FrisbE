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


WINDOWWIDTH = 600
WINDOWHEIGHT = 600

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Model:
    def __init__(self):
        self.robot = Robot()
        #self.course = ObstacleCourse()
        self.player = Player()
        
    def update(self):
        pass
    
class Actor:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Robot(Actor):
    def __init__(self):
        Actor.__init__(self, 100, 100, 100, 100)
        self.wheels = None
        self.shield = 5
        self.motor = None
        
class Queue:
    def __init__(self):
        self.stack = []
        
    def addAction(self,pos): #pos should be a tuple
        self.stack.append(pos)
        
class Player:
    def __init__(self):
        self.level = 0
        self.money = 100
        self.purchased = []

class Store:
    def __init__(self):
        self.inventory = []
        
class Upgrade:
    def __init__(self, name):
        self.name = name

class View:
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
         self.screen.fill(BLACK)
         pygame.draw.rect(self.screen, WHITE, self.model.robot.rect)
         

class Controller:
    def __init__(self, model):
        self.model = model
        
    def handleEvent(self, event):
       pass
                
            
if __name__ == '__main__':
    pygame.init()

    size = (WINDOWWIDTH,WINDOWHEIGHT)
    screen = pygame.display.set_mode(size)

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
        
    
    