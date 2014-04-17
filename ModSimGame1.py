# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 18:07:01 2014

@author: ndhanushkodi
"""
import sys

# Add current and parent directory. One of them is supposed to contain the
# planes package.
#
sys.path.append("../")
sys.path.append("./")

import pygame
import planes
import pdb
import time
import math
from collections import deque
from screen import Screen
from screen import Button
pygame.init()
from pygame.locals import *

WINDOWWIDTH = 1200
WINDOWHEIGHT = 800

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class ModSimGame:
    def __init__(self):
        self.currentscreen = ModSimScreen(self)




class ModSimScreen(Screen):
    def __init__(self,gamemodel):
        self.buttons = []
        button1 = RayButton("ray","ray.jpg",pygame.Rect(9*WINDOWWIDTH/10,0,WINDOWWIDTH/10,WINDOWWIDTH/10),RayButton.clicked, self)
        button2 = SharkButton("shark","shark.jpg",pygame.Rect(8*WINDOWWIDTH/10,0,WINDOWWIDTH/10,WINDOWWIDTH/10),SharkButton.clicked, self)
        self.buttons.append(button1)
        self.buttons.append(button2)
        Screen.__init__(self, self.buttons, [], (0,0,0))
    def update(self):
        pass
    
class RayButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWWIDTH/10))
        self.numRays = 0
        self.off = 0
        
    def clicked(self, button_name):
        print 'ray'
        #instantiate and put a ray on the gamescreen
        
        self.model.actors.append(Ray("rayA"+str(self.numRays), pygame.Rect(100,100+self.off,10,10), "ray.jpg"))
        self.numRays +=1  
        self.off += 10
        print self.numRays
        #remove self

class SharkButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWWIDTH/10))
        self.numSharks = 0
        self.off = 0
        
    def clicked(self, button_name):
        print 'shark'
        #instantiate and put a ray on the gamescreen

        self.model.actors.append(Shark("sharkA"+str(self.numSharks), pygame.Rect(120,100+self.off,10,10), "shark.jpg"))
        self.numSharks +=1  
        self.off += 10
        print self.numSharks
        #remove self

class Ray(planes.Plane):
    def __init__(self, name, rect, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        #print self
        #self.image = None
        self.image.fill((0,0,255))
        #self.rect = rect
        self.Xpos = rect.x
        self.Ypos = rect.y
    def clicked(self):
        pass

class Shark(planes.Plane):
    def __init__(self, name, rect, draggable = False, grab = True, ):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        #print self
        #self.image = None
        self.image.fill((0,255,0))
        #self.rect = rect
        self.Xpos = rect.x
        self.Ypos = rect.y
    def clicked(self):
        pass
  
#if __name__ == "__main__":
    
  
#class Animal_or_Event(Actor):
#    def __init__(self, x,y,width,height):
#        Actor.__init__(self,x,y,width,height,which_animalevent)
#        
#class PopulationGraph:
#
#class PopulationsModel:
#    def __init__(self):
#        self.width = 640
#        self.height = 480
#
#class PopulationsView:
#    def __init__(self, model, screen):
#        self.model = model
#        self.screen = screen
#    
#class PopulationsController:
#    def __init__(self, model, screen):
#        self.model = model
#        self.screen = screen
#        self.mouse_pos = (0,0)
#    
#        def handle_mouse_event(self, event):        
#        if event.type == MOUSEBUTTONDOWN:
#            self.mouse_pos = pygame.mouse.get_pos()