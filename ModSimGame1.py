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
from screen import ScreenText
pygame.init()
from pygame.locals import *

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

scrleft = 50
scrright = 1150
scrtop = 50
scrbottom = 700

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class ModSimGame:
    def __init__(self):
        self.modsimscreen = ModSimScreen(self)

        # start = StartButton("start","startbut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),StartButton.clicked, self)
        # settings = SettingsButton("settings","setbut.png",pygame.Rect(WINDOWWIDTH/8,6*WINDOWHEIGHT/8 + 30,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),SettingsButton.clicked, self)
        # tutorial = TutorialButton("tutorial","tutbut.png",pygame.Rect(WINDOWWIDTH/8,5*WINDOWHEIGHT/8 + 20,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),TutorialButton.clicked, self)
        # home = HomeButton("home","homebut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),HomeButton.clicked, self)
        # tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)
        # self.homescreen = Screen([start,settings,tutorial],[titleRect("home.png",tr,WHITE)],BLACK)
        # self.settingsscreen = Screen([home,settings,tutorial],[titleRect("settings.png",tr,WHITE)],BLACK)
        # self.tutorialscreen = Screen([home,settings, tutorial],[titleRect("tut.png",tr,WHITE)],BLACK)

        back = BackButton("back", "back_button_big.png", pygame.Rect(50,600,550,50), BackButton.clicked, self)
        start = StartButton("start","start_button.png",pygame.Rect(650,50,500,300),StartButton.clicked, self)
        tutorial = TutorialButton("tutorial","tutorial_button.png",pygame.Rect(650, 400, 500, 300),TutorialButton.clicked, self)
        home = HomeButton("home","title_button.png",pygame.Rect(650,50,500,300),HomeButton.clicked, self)
        tr = pygame.Rect(50, 50, 500, 575)
        self.homescreen = Screen([start,tutorial, back],[titleRect("robogame_logo.png",tr,WHITE)],BLACK)
        #self.tutorialscreen = Screen([home, tutorial],[titleRect("tut.png",tr,WHITE)],BLACK)
        self.tutorialscreen = Screen([],[titleRect("tut.png",tr,WHITE)],BLACK)

        self.currentscreen = self.homescreen
        self.toDash = False



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
        #self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))


class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.toDash = True



# class StartButton(Button):
#     def __init__(self, label, im, rect, callback, model):
#         Button.__init__(self, label, rect, callback, model)
#         self.image = pygame.image.load(im)
#     def clicked(self, button_name):
#         self.model.currentscreen = self.model.modsimscreen


# class HomeButton(Button):
#     def __init__(self, label, im, rect, callback, model):
#         Button.__init__(self, label, rect, callback, model)
#         self.image = pygame.image.load(im)
#     def clicked(self, button_name):
#         self.model.currentscreen = self.model.homescreen


# class SettingsButton(Button):
#     def __init__(self, label, im, rect, callback,model):
#         Button.__init__(self, label, rect, callback, model)
#         self.image = pygame.image.load(im)
#     def clicked(self, button_name):
#         self.model.currentscreen = self.model.settingsscreen


# class TutorialButton(Button):
#     def __init__(self, label, im, rect, callback, model):
#         Button.__init__(self, label, rect, callback, model)
#         self.image = pygame.image.load(im)
#     def clicked(self, button_name):
#         self.model.currentscreen = self.model.tutorialscreen


# class titleRect(planes.Plane):
#     def __init__(self, im, rect, color):
#         planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
#         self.image.fill(color)
#         self.rect = rect
#         self.color = color
#         self.image = pygame.image.load(im)



class ModSimScreen(Screen):
    def __init__(self,gamemodel):
        self.gamemodel = gamemodel
        self.buttons = []
        self.actors = []
        self.howManyRays = 0
        self.howManySharks = 0
        self.howManyScallops = 0
        self.howManyPlankton = 0
        self.howManyFishermen = 0
        self.howManyHurricanes = 0

        self.rayOffset = 0
        self.sharkOffset = 0
        self.scallopOffset = 0
        self.planktonOffset = 0
        self.fishermanOffset = 0
        self.hurricaneOffset = 0
        self.timesteps = 0

        font1 = pygame.font.SysFont("Arial", 40)
        self.timeLabel = ScreenText("timetext", "Timestep: "+str(self.timesteps), pygame.Rect(WINDOWWIDTH-270,0,250,50), font1)

        buttonReset = ResetButton("reset", "timestep_button.png", pygame.Rect(8*WINDOWWIDTH/10-40,8*WINDOWHEIGHT/10-30, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), ResetButton.clicked, self)
        button0 = TimeStepButton("time", "timestep_button.png", pygame.Rect(8*WINDOWWIDTH/10-40,7*WINDOWHEIGHT/10-40, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), TimeStepButton.clicked, self)
        button1 = RayButton("ray","ray.jpg",pygame.Rect(8*WINDOWWIDTH/10-30,WINDOWHEIGHT/10,WINDOWWIDTH/10,WINDOWHEIGHT/10),RayButton.clicked, self)
        button2 = SharkButton("shark","shark.jpg",pygame.Rect(9*WINDOWWIDTH/10-20,WINDOWHEIGHT/10,WINDOWWIDTH/10,WINDOWHEIGHT/10),SharkButton.clicked, self)
        button3 = ScallopButton("scallop", "scallop.jpg", pygame.Rect(8*WINDOWWIDTH/10-30,2*WINDOWHEIGHT/10, WINDOWWIDTH/10, WINDOWHEIGHT/10), ScallopButton.clicked, self)
        button4 = PlanktonButton("plankton", "plankton.jpeg", pygame.Rect(9*WINDOWWIDTH/10-20, 2*WINDOWHEIGHT/10, WINDOWWIDTH/10, WINDOWHEIGHT/10), PlanktonButton.clicked, self)
        button5 = FishermanButton("fisherman", "fisherman.jpg", pygame.Rect(8*WINDOWWIDTH/10-30, 3*WINDOWHEIGHT/10, WINDOWWIDTH/10, WINDOWHEIGHT/10), FishermanButton.clicked, self)                            
        button6 = HurricaneButton("hurricane", "hurricane.jpg", pygame.Rect(9*WINDOWWIDTH/10-20, 3*WINDOWHEIGHT/10, WINDOWWIDTH/10, WINDOWHEIGHT/10), HurricaneButton.clicked, self)
        
        ###########
        buttonback = GBackButton("back", "back_button_ingame.png", pygame.Rect(8*WINDOWWIDTH/10-40, 9*WINDOWHEIGHT/10-20, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), BackButton.clicked, self)
        self.buttons.append(buttonback)
        ##########
        self.buttons.append(buttonReset)
        self.buttons.append(button0)
        self.buttons.append(button1)
        self.buttons.append(button2)
        self.buttons.append(button3)
        self.buttons.append(button4)
        self.buttons.append(button5)
        self.buttons.append(button6)
        self.actors.append(self.timeLabel)
        Screen.__init__(self, self.buttons, self.actors, (0,0,0))

    def update(self):
        
        pass

    def reset(self):
        self.actors = []
        self.actors.append(self.timeLabel)

        self.rayOffset = 0
        self.sharkOffset = 0
        self.scallopOffset = 0
        self.planktonOffset = 0
        self.fishermanOffset = 0
        self.hurricaneOffset = 0

        self.howManyRays = 0
        self.howManySharks = 0
        self.howManyScallops = 0
        self.howManyPlankton = 0
        self.howManyFishermen = 0
        self.howManyHurricanes = 0
        print 'reset '

    def updateEnv(self):
        self.actors = []
        self.actors.append(self.timeLabel)

        ############MODEL CONSTANTS############
        # A0 = self.howManyScallops*10000
        # R0 = self.howManyRays*10000
        P0 = self.howManyPlankton*5000
        A0 = self.howManyScallops*5000
        R0 = self.howManyRays*5000
        #S0 = self.howManySharks*500
        S0 = self.howManySharks*5000

        # Ca = 2000000 #might want to remove some zeroes
        # Cr = 1500000
        Cp = 3000000
        Ca = 2000000
        Cr = 1000000
        Cs = 1000000
        #Cs = 50000
        #Cs = 800000

        # Ac = 60000
        # Rc = 50000
        Pc = 500000
        Ac = 300000
        Rc = 20000
        #Sc = 1100
        Sc = 11000

        # betaA = .12
        # betaR = .11
        # betaS = .10

        ##############MODEL#####################
        betaP = .2
        betaA = .15
        betaR = .14
        betaS = .13

        #deltascallops = A0*((1-(A0/Ca)))*(1-(R0/Rc))*betaA
        deltaplankton = P0*((1-(P0/Cp)))*(1-(R0/Rc))*betaP
        deltascallops = A0*((1-(A0/Ca)))*((P0/Pc)-(R0/Rc))*betaA
        deltarays = R0*(1-(R0/Cr))*((A0/Ac)-(S0/Sc))*betaR
        deltasharks = S0*(1-S0/Cs)*(-1+(R0/Rc))*betaS

        P1 = P0 + deltaplankton
        A1 = A0 + deltascallops
        R1 = R0 + deltarays
        S1 = S0 + deltasharks
        #########################################
        
        self.timeLabel.updateText("Timestep: " + str(self.timesteps))
        self.rayOffset = 0
        self.sharkOffset = 0
        self.scallopOffset = 0
        self.planktonOffset = 0
        self.fishermanOffset = 0
        self.hurricaneOffset = 0

        self.howManyRays = int(R1/5000)
        #self.howManySharks = int(S1/500)
        self.howManySharks = int(S1/5000)
        self.howManyScallops = int(A1/5000)
        self.howManyPlankton = int(P1/5000)
        self.howManyFishermen = 0
        self.howManyHurricanes = 0

        for i in range(1,self.howManyRays+1):
            
            self.actors.append(Ray("rayA"+str(i), pygame.Rect(100,100+self.rayOffset,10,10), "ray.jpg", self))
            self.rayOffset +=10
        print 'rays ' + str(self.howManyRays)

        for i in range(1,self.howManySharks+1):

            self.actors.append(Shark("sharkA"+str(i), pygame.Rect(220,100+self.sharkOffset,10,10), "shark.jpg", self))
            self.sharkOffset +=10
        print 'sharks ' + str(self.howManySharks)

        for i in range(1,self.howManyScallops+1):
            
            self.actors.append(Scallop("scallopA"+str(i), pygame.Rect(340,100+self.scallopOffset,10,10), "scallop.jpg", self))
            self.scallopOffset +=10
        print 'scallops ' + str(self.howManyScallops)

        for i in range(1,self.howManyPlankton+1):
            
            self.actors.append(Plankton("planktonA"+str(i), pygame.Rect(460,100+self.planktonOffset,10,10), "plankton.jpeg", self))
            self.planktonOffset +=10
        print 'plankton ' + str(self.howManyPlankton)


        #equations in for loops
        #self.actors.append(Ray("rayA"+str(self.howManyRays), pygame.Rect(100,100+self.rayOffset,10,10), "ray.jpg", self))
        #self.howManyRays+=1
        #print 'rays ' + str(self.howManyRays)
        #self.rayOffset += 10


class ResetButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        #self.image = pygame.image.load(im)
        #self.image = pygame.transform.scale(pygame.image.load(im), (50,10))
        self.image.fill((255,10,75))

    def clicked(self, button_name):
        self.model.reset()

class TimeStepButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
        #self.image = pygame.transform.scale(pygame.image.load(im), (50,10))
        #self.image.fill((100,10,75))

    def clicked(self, button_name):
        self.model.timesteps +=1
        print 'timestep ' + str(self.model.timesteps)
        self.model.updateEnv()



###############################################################################
class GBackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
        #self.image.fill((0,0,255))
    def clicked(self, button_name):
        self.model.gamemodel.currentscreen = self.model.gamemodel.homescreen
###############################################################################



class RayButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        #instantiate and put a ray on the gamescreen     
        self.model.howManyRays +=1    

        self.model.actors.append(Ray("rayA"+str(self.model.howManyRays), pygame.Rect(100,100+self.model.rayOffset,10,10), "ray.jpg",self.model))
        self.model.rayOffset += 10
        print 'rays ' + str(self.model.howManyRays)
      


class SharkButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
        
    def clicked(self, button_name):
        self.model.howManySharks +=1  

        self.model.actors.append(Shark("sharkA"+str(self.model.howManySharks), pygame.Rect(220,100+self.model.sharkOffset,10,10), "shark.jpg", self.model))
        self.model.sharkOffset += 10
        print 'sharks ' + str(self.model.howManySharks)



class ScallopButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        self.model.howManyScallops +=1 
     
        self.model.actors.append(Scallop("scallopA"+str(self.model.howManyScallops), pygame.Rect(340,100+self.model.scallopOffset,10,10), "scallop.jpg",self.model))
        self.model.scallopOffset += 10  
        print 'scallops ' + str(self.model.howManyScallops)



class PlanktonButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        self.model.howManyPlankton +=1 
     
        self.model.actors.append(Plankton("planktonA"+str(self.model.howManyPlankton), pygame.Rect(460,100+self.model.planktonOffset,10,10), "plankton.jpeg",self.model))
        self.model.planktonOffset += 10 
        print 'plankton ' + str(self.model.howManyPlankton)



class FishermanButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        self.model.howManyFishermen +=1 
     
        self.model.actors.append(Fisherman("fishermanA"+str(self.model.howManyFishermen), pygame.Rect(580,100+self.model.fishermanOffset,10,10), "fisherman.jpg",self.model))
        self.model.fishermanOffset += 10 
        print 'fishermen ' + str(self.model.howManyFishermen)



class HurricaneButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        self.model.howManyHurricanes +=1 
   
        self.model.actors.append(Hurricane("hurricaneA"+str(self.model.howManyHurricanes), pygame.Rect(700,100+self.model.hurricaneOffset,10,10), "hurricane.jpg",self.model))
        self.model.hurricaneOffset += 10   
        print 'hurricane ' + str(self.model.howManyHurricanes)



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



class Fisherman(planes.Plane):
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
            self.model.fishermanOffset -= 10
            self.model.howManyFishermen -=1  



class Hurricane(planes.Plane):
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
            self.model.hurricaneOffset -= 10
            self.model.howManyHurricanes -=1  