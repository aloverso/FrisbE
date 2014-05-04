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

        back = BackButton("back", "back_button_long.png", pygame.Rect(50,600,550,50), BackButton.clicked, self)
        start = StartButton("start","start_button.png",pygame.Rect(650,50,500,300),StartButton.clicked, self)
        tutorial = TutorialButton("tutorial","tutorial_button.png",pygame.Rect(650, 400, 500, 300),TutorialButton.clicked, self)
        home = HomeButton("home","title_button.png",pygame.Rect(650,50,500,300),HomeButton.clicked, self)
        home2 = HomeButton("home","title_button.png",pygame.Rect(650,250,500,300),HomeButton.clicked, self)

        tr = pygame.Rect(50, 50, 500, 500)
        tr2 = pygame.Rect(50, 10, 500, 730)
        # MAKE LOGO 500 by 575
        self.homescreen = Screen([start,tutorial, back],[titleRect("modsim_logo.png",tr,WHITE)],BLACK)
        self.tutorialscreen = Screen([home2],[titleRect2("tutorial_modsim.png",tr2,WHITE)],BLACK)
        #self.tutorialscreen = Screen([],[titleRect("tut.png",tr,WHITE)],BLACK)

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

class titleRect2(planes.Plane):
    def __init__(self, im, rect, color):
        planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
        self.image.fill(color)
        self.rect = rect
        self.color = color
        #self.image = pygame.image.load(im)
        self.image = pygame.transform.scale(pygame.image.load(im), (500,730))


class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.toDash = True



class ModSimScreen(Screen):
    def __init__(self,gamemodel):

        self.gamemodel = gamemodel
        self.buttons = []
        self.actors = []
        self.howManyRays = 0
        self.howManySharks = 0
        self.howManyScallops = 0
        #self.howManyPlankton = 0


        self.rayOffset = 0
        self.sharkOffset = 0
        self.scallopOffset = 0

        self.rayX = 0
        self.sharkX = 0
        self.scallopX = 0
        #self.planktonOffset = 0

        self.timesteps = 0

        font1 = pygame.font.SysFont("Arial", 20)
        self.timeLabel = ScreenText("timetext", "Timestep: "+str(self.timesteps), pygame.Rect(WINDOWWIDTH-270,0,250,40), font1)
        self.numrayLabel = ScreenText("raytext", "Rays: "+str(self.howManyRays), pygame.Rect(70,0,100,30), font1)
        self.changerayLabel = ScreenText("changeraytext", "Change: "+str(self.howManyRays), pygame.Rect(70,40,100,30), font1)
        self.numsharkLabel = ScreenText("sharktext", "Sharks: "+str(self.howManySharks), pygame.Rect(300,0,100,30), font1)
        self.changesharkLabel = ScreenText("changesharktext", "Change: "+str(self.howManySharks), pygame.Rect(300,40,100,30), font1)
        self.numscallopLabel = ScreenText("scalloptext", "Scallops: "+str(self.howManyScallops), pygame.Rect(530,0,100,30), font1)
        self.changescallopLabel = ScreenText("changescalloptext", "Change: "+str(self.howManyScallops), pygame.Rect(530,40,100,30), font1)
        #self.numplanktonLabel = ScreenText("planktontext", "Plankton: "+str(self.howManyPlankton), pygame.Rect(410,0,100,40), font1)
        #self.changeplanktonLabel = ScreenText("changeplanktontext", "Change: "+str(self.howManyPlankton), pygame.Rect(410,40,100,40), font1)

        buttonReset = ResetButton("reset", "reset_button.png", pygame.Rect(8*WINDOWWIDTH/10-40,8*WINDOWHEIGHT/10-30, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), ResetButton.clicked, self)
        button0 = TimeStepButton("time", "timestep_button.png", pygame.Rect(8*WINDOWWIDTH/10-40,7*WINDOWHEIGHT/10-40, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), TimeStepButton.clicked, self)
        button1 = RayButton("ray","ray.png",pygame.Rect(8*WINDOWWIDTH/10-30,WINDOWHEIGHT/10,WINDOWWIDTH/10,WINDOWHEIGHT/10),RayButton.clicked, self)
        button2 = SharkButton("shark","shark.png",pygame.Rect(9*WINDOWWIDTH/10-20,WINDOWHEIGHT/10,WINDOWWIDTH/10,WINDOWHEIGHT/10),SharkButton.clicked, self)
        button3 = ScallopButton("scallop", "scallop.png", pygame.Rect(8*WINDOWWIDTH/10-30,2*WINDOWHEIGHT/10, WINDOWWIDTH/10, WINDOWHEIGHT/10), ScallopButton.clicked, self)
        #button4 = PlanktonButton("plankton", "plankton.jpeg", pygame.Rect(9*WINDOWWIDTH/10-20, 2*WINDOWHEIGHT/10, WINDOWWIDTH/10, WINDOWHEIGHT/10), PlanktonButton.clicked, self)
        
        ###########
        buttonback = GBackButton("back", "back_button_ingame.png", pygame.Rect(8*WINDOWWIDTH/10-40, 9*WINDOWHEIGHT/10-20, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), BackButton.clicked, self)
        self.buttons.append(buttonback)
        ##########
        self.buttons.append(buttonReset)
        self.buttons.append(button0)
        self.buttons.append(button1)
        self.buttons.append(button2)
        self.buttons.append(button3)
        #self.buttons.append(button4)

        self.actors.append(self.timeLabel)
        self.actors.append(self.numrayLabel)
        self.actors.append(self.changerayLabel)
        self.actors.append(self.numsharkLabel)
        self.actors.append(self.changesharkLabel)
        self.actors.append(self.numscallopLabel)
        self.actors.append(self.changescallopLabel)
        #self.actors.append(self.numplanktonLabel)
        #self.actors.append(self.changeplanktonLabel)
        Screen.__init__(self, self.buttons, self.actors, "Background_modsim.png")
        #Screen.__init__(self, self.buttons, self.actors, "underwater.jpg")

    def update(self):


        pass

    def reset(self):
        self.actors = []
        self.actors.append(self.timeLabel)
        self.actors.append(self.numrayLabel)
        self.actors.append(self.changerayLabel)
        self.actors.append(self.numsharkLabel)
        self.actors.append(self.changesharkLabel)
        self.actors.append(self.numscallopLabel)
        self.actors.append(self.changescallopLabel)
        #self.actors.append(self.numplanktonLabel)
        #self.actors.append(self.changeplanktonLabel)

        self.rayOffset = 0
        self.sharkOffset = 0
        self.scallopOffset = 0

        self.rayX = 0
        self.sharkX = 0
        self.scallopX = 0
        #self.planktonOffset = 0


        self.howManyRays = 0
        self.howManySharks = 0
        self.howManyScallops = 0
        #self.howManyPlankton = 0

        self.numrayLabel.updateText("Rays: " + str(self.howManyRays))
        self.changerayLabel.updateText("Change: " + str(0))
        self.numsharkLabel.updateText("Sharks: " + str(self.howManySharks))
        self.changesharkLabel.updateText("Change: " + str(0))
        self.numscallopLabel.updateText("Scallops: " + str(self.howManyScallops))
        self.changescallopLabel.updateText("Change: " + str(0))
        #self.numplanktonLabel.updateText("Plankton: " + str(self.howManyPlankton))
        #self.changeplanktonLabel.updateText("Change: " + str(0))

        self.timesteps = 0
        print 'reset '

    def updateEnv(self):
        self.actors = []
        self.actors.append(self.timeLabel)
        self.actors.append(self.numrayLabel)
        self.actors.append(self.changerayLabel)
        self.actors.append(self.numsharkLabel)
        self.actors.append(self.changesharkLabel)
        self.actors.append(self.numscallopLabel)
        self.actors.append(self.changescallopLabel)
        #self.actors.append(self.numplanktonLabel)
        #self.actors.append(self.changeplanktonLabel)

        rays_t_minus_1 = self.howManyRays
        sharks_t_minus_1 = self.howManySharks
        scallops_t_minus_1 = self.howManyScallops
        #plankton_t_minus_1 = self.howManyPlankton

        ############MODEL CONSTANTS############
        # A0 = self.howManyScallops*10000
        # R0 = self.howManyRays*10000
        #P0 = self.howManyPlankton*5000
        A0 = self.howManyScallops*5000
        R0 = self.howManyRays*5000
        #S0 = self.howManySharks*500
        S0 = self.howManySharks*5000

        # Ca = 2000000 #might want to remove some zeroes
        # Cr = 1500000
        #Cp = 20000000
        Ca = 20000000
        Cr = 10000000
        Cs = 10000000
        #Cs = 50000
        #Cs = 800000

        # Ac = 60000
        # Rc = 50000
        #Pc = 100000
        Ac = 100000
        Rc = 100000
        #Sc = 1100
        Sc = 100000

        # betaA = .12
        # betaR = .11
        # betaS = .10

        ##############MODEL#####################
        #betaP = .2
        betaA = .15
        betaR = .14
        betaS = .13

        #deltascallops = A0*(1-A0/Ca)*(-1 + (P0/Pc))*betaA
        #deltaplankton = P0*(1-P0/Cp)*(betaP-.2)
        #deltascallops = A0*(1-A0/Ca)*(-betaA*P0 + .1)
        #deltascallops = A0*((1-(A0/Ca))*((P0/Pc)-(R0/Rc)))*betaA
        #deltascallops = A0*(1-(A0/Ca))*(-1+(P0/Pc))*(-1 + (R0/Rc))*betaA
        #deltarays = R0*(1-(R0/Cr))*(-1 +(A0/Ac))*(-1+(S0/Sc))*betaR

        #deltaplankton = P0*((1-(P0/Cp))*(-1 + (A0/Ac)))*betaP

        #deltascallops = A0*((1-(A0/Ca)))*(1-(R0/Rc))*betaA

        #deltarays = R0*(1-(R0/Cr))*((A0/Ac)-(S0/Sc))*betaR

        #deltasharks = S0*(1-S0/Cs)*(-1+(R0/Rc))*betaS

        if R0>A0/4.0:
            deltascallops = -5000
            deltarays = -5000
        if R0>A0/2.2:
            deltascallops = -10000
            deltarays = -10000
        if R0>A0/1.7:
            deltascallops = -15000
            deltarays = -15000
        if R0>A0/1.2:
            deltascallops = -A0
            deltarays = -20000
        if A0/4.0>=R0:
            deltascallops = 5000
            deltarays = 5000
        if A0/8.0>R0:
            deltascallops = 10000
            deltarays = 10000
        if A0/16.0>R0:
            deltascallops = 15000
            deltarays = 10000

        if S0>R0/4:
            deltarays += -5000
            deltasharks = -5000
        if S0>R0/2.2:
            deltarays += -10000
            deltasharks = -10000
        if S0>R0/1.7:
            deltarays += -15000
            deltasharks = -15000
        if S0>R0/1.2:
            deltarays += -R0
            deltasharks = -20000
        if R0/4>=S0:
            deltarays += 5000
            deltasharks = 5000
        if R0/8>S0:
            deltarays += 10000
            deltasharks = 10000
        if R0/16>S0:
            deltarays += 15000
            deltasharks = 10000

        if A0 == 0:
            deltascallops = 0

        if R0 == 0:
            deltarays = 0

        if S0 == 0:
            deltasharks = 0





        #P1 = P0 + deltaplankton
        A1 = A0 + deltascallops
        R1 = R0 + deltarays
        S1 = S0 + deltasharks

        if A1<0:
            A1 = 0
        if R1<0:
            R1 = 0
        if S1<0:
            S1 = 0
        #########################################
        
        self.timeLabel.updateText("Timestep: " + str(self.timesteps))
        self.rayOffset = 0
        self.sharkOffset = 0
        self.scallopOffset = 0
        #self.planktonOffset = 0


        self.howManyRays = int(R1/5000)
        #self.howManySharks = int(S1/500)
        self.howManySharks = int(S1/5000)
        self.howManyScallops = int(A1/5000)
        #self.howManyPlankton = int(P1/5000)


        self.changeInRays = (self.howManyRays-rays_t_minus_1)
        self.changeInSharks = (self.howManySharks-sharks_t_minus_1)
        self.changeInScallops = (self.howManyScallops-scallops_t_minus_1)
        #self.changeInPlankton = (self.howManyPlankton-plankton_t_minus_1)

        self.numrayLabel.updateText("Rays: " + str(self.howManyRays))
        self.changerayLabel.updateText("Change: " + str(self.changeInRays))
        self.numsharkLabel.updateText("Sharks: " + str(self.howManySharks))
        self.changesharkLabel.updateText("Change: " + str(self.changeInSharks))
        self.numscallopLabel.updateText("Scallops: " + str(self.howManyScallops))
        self.changescallopLabel.updateText("Change: " + str(self.changeInScallops))
        #self.numplanktonLabel.updateText("Plankton: " + str(self.howManyPlankton))
        #self.changeplanktonLabel.updateText("Change: " + str(self.changeInPlankton))

        for i in range(1,self.howManyRays+1):
            
            self.actors.append(Ray("rayA"+str(i), pygame.Rect(100+self.rayX,100+self.rayOffset,10,10), "ray.jpg", self))
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

        # for i in range(1,self.howManyPlankton+1):
            
        #     self.actors.append(Plankton("planktonA"+str(i), pygame.Rect(460,100+self.planktonOffset,10,10), "plankton.jpeg", self))
        #     self.planktonOffset +=10
        # print 'plankton ' + str(self.howManyPlankton)



class ResetButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        #self.image = pygame.image.load(im)
        self.image = pygame.transform.scale(pygame.image.load(im), (240,75))
        #self.image.fill((255,10,75))

    def clicked(self, button_name):
        self.model.reset()

class TimeStepButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
        #self.image = pygame.transform.scale(pygame.image.load(im), (50,10))

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

        self.model.actors.append(Ray("rayA"+str(self.model.howManyRays), pygame.Rect(100,100+self.model.rayOffset,10,10), "ray.png",self.model))
        self.model.rayOffset += 10
        print 'rays ' + str(self.model.howManyRays)
        self.model.numrayLabel.updateText("Rays: " + str(self.model.howManyRays))
      


class SharkButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
        
    def clicked(self, button_name):
        self.model.howManySharks +=1  

        self.model.actors.append(Shark("sharkA"+str(self.model.howManySharks), pygame.Rect(220,100+self.model.sharkOffset,10,10), "shark.png", self.model))
        self.model.sharkOffset += 10
        print 'sharks ' + str(self.model.howManySharks)
        self.model.numsharkLabel.updateText("Sharks: " + str(self.model.howManySharks))


class ScallopButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        self.model.howManyScallops +=1 
     
        self.model.actors.append(Scallop("scallopA"+str(self.model.howManyScallops), pygame.Rect(340,100+self.model.scallopOffset,10,10), "scallop.png",self.model))
        self.model.scallopOffset += 10  
        print 'scallops ' + str(self.model.howManyScallops)
        self.model.numscallopLabel.updateText("Scallops: " + str(self.model.howManyScallops))



# class PlanktonButton(Button):
#     def __init__(self, label, im, rect, callback, model):
#         Button.__init__(self, label, rect, callback, model)
#         self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
#     def clicked(self, button_name):
#         self.model.howManyPlankton +=1 
     
#         self.model.actors.append(Plankton("planktonA"+str(self.model.howManyPlankton), pygame.Rect(460,100+self.model.planktonOffset,10,10), "plankton.jpeg",self.model))
#         self.model.planktonOffset += 10 
#         print 'plankton ' + str(self.model.howManyPlankton)
#         self.model.numplanktonLabel.updateText("Plankton: " + str(self.model.howManyPlankton))



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
            self.model.numrayLabel.updateText("Rays: " + str(self.model.howManyRays))



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




# class Plankton(planes.Plane):
#     def __init__(self, name, rect, im, model, draggable = False, grab = True):
#         planes.Plane.__init__(self, name, rect, draggable, grab)

#         self.image = pygame.transform.scale(pygame.image.load(im), (10,10))
#         self.Xpos = rect.x
#         self.Ypos = rect.y
#         self.model = model

#     def clicked(self, button_name):
#         names = [actor.name for actor in self.model.actors]
#         if self.name in names:
#             index = names.index(self.name)
#             del(self.model.actors[index])
#             self.model.planktonOffset -= 10
#             self.model.howManyPlankton -=1  


 