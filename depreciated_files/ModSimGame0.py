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
        self.modsimscreen = ModSimScreen(self)

        start = StartButton("start","startbut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),StartButton.clicked, self)
        settings = SettingsButton("settings","setbut.png",pygame.Rect(WINDOWWIDTH/8,6*WINDOWHEIGHT/8 + 30,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),SettingsButton.clicked, self)
        tutorial = TutorialButton("tutorial","tutbut.png",pygame.Rect(WINDOWWIDTH/8,5*WINDOWHEIGHT/8 + 20,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),TutorialButton.clicked, self)
        home = HomeButton("home","homebut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),HomeButton.clicked, self)
        tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)
        self.homescreen = Screen([start,settings,tutorial],[titleRect("home.png",tr,WHITE)],BLACK)
        self.settingsscreen = Screen([home,settings,tutorial],[titleRect("settings.png",tr,WHITE)],BLACK)
        self.tutorialscreen = Screen([home,settings, tutorial],[titleRect("tut.png",tr,WHITE)],BLACK)
        self.currentscreen = self.homescreen
        

class StartButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.modsimscreen

class HomeButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.homescreen

class SettingsButton(Button):
    def __init__(self, label, im, rect, callback,model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.settingsscreen

class TutorialButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.tutorialscreen

class titleRect(planes.Plane):
    def __init__(self, im, rect, color):
        planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
        self.image.fill(color)
        self.rect = rect
        self.color = color
        self.image = pygame.image.load(im)

class ModSimScreen(Screen):
    def __init__(self,gamemodel):
        self.buttons = []
        self.howManyRays = 0
        self.howManySharks = 0
        self.howManyScallops = 0
        self.rayOffset = 10
        self.sharkOffset = 10
        self.timesteps = 0
        button0 = TimeStepButton("time", "ray.jpg", pygame.Rect(8.5*WINDOWWIDTH/10,8*WINDOWHEIGHT/10, WINDOWWIDTH/10, WINDOWHEIGHT/10), TimeStepButton.clicked, self)
        button1 = RayButton("ray","ray.jpg",pygame.Rect(9*WINDOWWIDTH/10,0,WINDOWWIDTH/10,WINDOWWIDTH/10),RayButton.clicked, self)
        button2 = SharkButton("shark","shark.jpg",pygame.Rect(8*WINDOWWIDTH/10,0,WINDOWWIDTH/10,WINDOWWIDTH/10),SharkButton.clicked, self)
        self.buttons.append(button0)
        self.buttons.append(button1)
        self.buttons.append(button2)
        Screen.__init__(self, self.buttons, [], (0,0,0))
    def update(self):
        pass
    def updateEnv(self):
        #for i in range(len(self.actors)-1):
         #   del(self.actors[i])
        self.actors = []
        self.rayOffset = 0
        self.actors.append(Ray("rayA"+str(self.howManyRays), pygame.Rect(100,100+self.rayOffset,10,10), "ray.jpg", self))
        self.howManyRays+=1
        print 'rays ' + str(self.howManyRays)
        self.rayOffset += 10

    #def removeActor(self,which_actor):
        #self.actors.remove(which_actor)

        #actIndex = self.actors.index(which_actor.name)
        #self.actors.remove(actIndex)
        #self.remove()

class TimeStepButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        #self.image = pygame.transform.scale(pygame.image.load(im), (50,10))
        self.image.fill((50,10,75))

    def clicked(self, button_name):
        print 'timestep'
        self.model.timesteps +=1
        print self.model.timesteps
        self.model.updateEnv()
        # numRays*=2
        # RayButton.clicked()


class RayButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWWIDTH/10))
       
    def clicked(self, button_name):
        print 'ray'
        #instantiate and put a ray on the gamescreen
        self.model.howManyRays +=1 
        self.model.actors.append(Ray("rayA"+str(self.model.howManyRays), pygame.Rect(100,100+self.model.rayOffset,10,10), "ray.jpg",self.model))

        self.model.rayOffset += 10
        print self.model.howManyRays
        #remove self

class SharkButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWWIDTH/10))
        
    def clicked(self, button_name):
        print 'shark'
        #instantiate and put a ray on the gamescreen

        self.model.actors.append(Shark("sharkA"+str(self.model.howManySharks), pygame.Rect(120,100+self.model.sharkOffset,10,10), "shark.jpg"))
        self.model.howManySharks +=1  
        self.model.sharkOffset += 10
        print self.model.howManySharks
        #remove self

class Ray(planes.Plane):
    def __init__(self, name, rect, im, model, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        #print self
        #self.image = None
        #self.image.fill((0,0,255))
        self.image = pygame.transform.scale(pygame.image.load(im), (10,10))
        #self.rect = rect
        self.Xpos = rect.x
        self.Ypos = rect.y
        self.model = model

    def clicked(self, button_name):
        names = [actor.name for actor in self.model.actors]
        if self.name in names:
            index = names.index(self.name)
            del(self.model.actors[index])
            self.model.rayOffset -= 10
            self.model.howManyRays -=1
        #pass
        #self.model.removeActor(self)
        # index = self.model.actors.index(self)
        # self.model.actors[index] = None

class Shark(planes.Plane):
    def __init__(self, name, rect, draggable = False, grab = True, ):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        #print self
        #self.image = None
        self.image.fill((0,255,0))
        #self.rect = rect
        self.Xpos = rect.x
        self.Ypos = rect.y
    def clicked(self, button_name):
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