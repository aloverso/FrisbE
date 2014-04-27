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
WINDOWHEIGHT = 750

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
        self.gamemodel = gamemodel
        self.buttons = []
        self.howManyRays = 0
        self.howManySharks = 0
        self.howManyScallops = 0
        self.howManyPlankton = 0
        self.rayOffset = 10
        self.sharkOffset = 10
        self.scallopOffset = 10
        self.planktonOffset = 10
        self.timesteps = 0

        button0 = TimeStepButton("time", "ray.jpg", pygame.Rect(8*WINDOWWIDTH/10,8*WINDOWHEIGHT/10, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), TimeStepButton.clicked, self)
        button1 = RayButton("ray","ray.jpg",pygame.Rect(8*WINDOWWIDTH/10,WINDOWHEIGHT/10,WINDOWWIDTH/10,WINDOWHEIGHT/10),RayButton.clicked, self)
        button2 = SharkButton("shark","shark.jpg",pygame.Rect(9*WINDOWWIDTH/10,WINDOWHEIGHT/10,WINDOWWIDTH/10,WINDOWHEIGHT/10),SharkButton.clicked, self)
        button3 = ScallopButton("scallop", "scallop.jpg", pygame.Rect(8*WINDOWWIDTH/10,2*WINDOWHEIGHT/10, WINDOWWIDTH/10, WINDOWHEIGHT/10), ScallopButton.clicked, self)
        button4 = PlanktonButton("plankton", "plankton.jpeg", pygame.Rect(9*WINDOWWIDTH/10, 2*WINDOWHEIGHT/10, WINDOWWIDTH/10, WINDOWHEIGHT/10), PlanktonButton.clicked, self)
        button5 = FishermanButton("fisherman", "fisherman.jpg")
        ###########
        buttonback = BackButton("back", "ray.jpg", pygame.Rect(8*WINDOWWIDTH/10, 9*WINDOWHEIGHT/10, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), BackButton.clicked, self)
        self.buttons.append(buttonback)
        ##########

        self.buttons.append(button0)
        self.buttons.append(button1)
        self.buttons.append(button2)
        self.buttons.append(button3)
        self.buttons.append(button4)
        #fisherman
        #
        Screen.__init__(self, self.buttons, [], (0,0,0))

    def update(self):
        pass

    def updateEnv(self):
        self.actors = []
        self.howManyRays = 0
        self.howManySharks = 0
        self.howManyScallops = 0
        self.howManyPlankton = 0

        self.rayOffset = 0
        self.sharkOffset = 0
        self.scallopOffset = 0
        self.planktonOffset = 0

        #equations in for loops
        self.actors.append(Ray("rayA"+str(self.howManyRays), pygame.Rect(100,100+self.rayOffset,10,10), "ray.jpg", self))
        self.howManyRays+=1
        print 'rays ' + str(self.howManyRays)
        self.rayOffset += 10



class TimeStepButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        #self.image = pygame.transform.scale(pygame.image.load(im), (50,10))
        self.image.fill((100,10,75))

    def clicked(self, button_name):
        print 'timestep'
        self.model.timesteps +=1
        print self.model.timesteps
        self.model.updateEnv()



###############################################################################
class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image.fill((0,0,255))
    def clicked(self, button_name):
        self.model.gamemodel.currentscreen = self.model.gamemodel.homescreen
###############################################################################



class RayButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        #instantiate and put a ray on the gamescreen        
        self.model.actors.append(Ray("rayA"+str(self.model.howManyRays), pygame.Rect(100,100+self.model.rayOffset,10,10), "ray.jpg",self.model))
        self.model.howManyRays +=1 
        self.model.rayOffset += 10
        print 'rays ' + str(self.model.howManyRays)
      


class SharkButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
        
    def clicked(self, button_name):

        self.model.actors.append(Shark("sharkA"+str(self.model.howManySharks), pygame.Rect(140,100+self.model.sharkOffset,10,10), "shark.jpg", self.model))
        self.model.howManySharks +=1  
        self.model.sharkOffset += 10
        print 'sharks ' + str(self.model.howManySharks)



class ScallopButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        #instantiate and put a ray on the gamescreen        
        self.model.actors.append(Scallop("scallopA"+str(self.model.howManyScallops), pygame.Rect(180,100+self.model.scallopOffset,10,10), "scallop.jpg",self.model))
        self.model.howManyScallops +=1 
        self.model.scallopOffset += 10
        print 'scallops ' + str(self.model.howManyScallops)



class PlanktonButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        #instantiate and put a ray on the gamescreen        
        self.model.actors.append(Plankton("planktonA"+str(self.model.howManyPlankton), pygame.Rect(220,100+self.model.planktonOffset,10,10), "plankton.jpeg",self.model))
        self.model.howManyPlankton +=1 
        self.model.planktonOffset += 10
        print 'plankton ' + str(self.model.howManyPlankton)



class Ray(planes.Plane):
    def __init__(self, name, rect, im, model, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)

        self.image = pygame.transform.scale(pygame.image.load(im), (10,10))
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



class Shark(planes.Plane):
    def __init__(self, name, rect, im, model, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)

        self.image = pygame.transform.scale(pygame.image.load(im), (10,10))
        self.Xpos = rect.x
        self.Ypos = rect.y
        self.model = model

    def clicked(self, button_name):
        names = [actor.name for actor in self.model.actors]
        if self.name in names:
            index = names.index(self.name)
            del(self.model.actors[index])
            self.model.sharkOffset -= 10
            self.model.howManySharks -=1



class Scallop(planes.Plane):
    def __init__(self, name, rect, im, model, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)

        self.image = pygame.transform.scale(pygame.image.load(im), (10,10))
        self.Xpos = rect.x
        self.Ypos = rect.y
        self.model = model

    def clicked(self, button_name):
        names = [actor.name for actor in self.model.actors]
        if self.name in names:
            index = names.index(self.name)
            del(self.model.actors[index])
            self.model.scallopOffset -= 10
            self.model.howManyScallops -=1



class Plankton(planes.Plane):
    def __init__(self, name, rect, im, model, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)

        self.image = pygame.transform.scale(pygame.image.load(im), (10,10))
        self.Xpos = rect.x
        self.Ypos = rect.y
        self.model = model

    def clicked(self, button_name):
        names = [actor.name for actor in self.model.actors]
        if self.name in names:
            index = names.index(self.name)
            del(self.model.actors[index])
            self.model.planktonOffset -= 10
            self.model.howManyPlankton -=1  