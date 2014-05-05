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
        self.image = pygame.transform.scale(pygame.image.load(im), (500,500))

class titleRect2(planes.Plane):
    def __init__(self, im, rect, color):
        planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
        self.image.fill(color)
        self.rect = rect
        self.color = color

        self.image = pygame.transform.scale(pygame.image.load(im), (500,730))


class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.toDash = True



class ModSimScreen(Screen):
    def __init__(self,gamemodel):

        self.win = 0
        self.gamemodel = gamemodel
        self.buttons = []
        self.actors = []
        self.howManyRays = 0
        self.howManySharks = 0
        self.howManyScallops = 0



        self.rayOffset = 0
        self.sharkOffset = 0
        self.scallopOffset = 0

        self.rayX = 0
        self.sharkX = 0
        self.scallopX = 0

        self.timesteps = 0

        font1 = pygame.font.SysFont("Arial", 20)
        font2 = pygame.font.SysFont("Arial", 70)
        self.timeLabel = ScreenText("timetext", "Timestep: "+str(self.timesteps), pygame.Rect(WINDOWWIDTH-270,0,250,40), font1)
        self.numrayLabel = ScreenText("raytext", "Rays: "+str(self.howManyRays), pygame.Rect(70,0,150,30), font1)
        self.changerayLabel = ScreenText("changeraytext", "Change: "+str(self.howManyRays), pygame.Rect(70,40,150,30), font1)
        self.numsharkLabel = ScreenText("sharktext", "Sharks: "+str(self.howManySharks), pygame.Rect(300,0,150,30), font1)
        self.changesharkLabel = ScreenText("changesharktext", "Change: "+str(self.howManySharks), pygame.Rect(300,40,150,30), font1)
        self.numscallopLabel = ScreenText("scalloptext", "Scallops: "+str(self.howManyScallops), pygame.Rect(530,0,150,30), font1)
        self.changescallopLabel = ScreenText("changescalloptext", "Change: "+str(self.howManyScallops), pygame.Rect(530,40,150,30), font1)

        self.winLabel = ScreenText("wintext", "YOU WIN!", pygame.Rect(0,0,1200,750), font2)
        buttonReset = ResetButton("reset", "reset_button.png", pygame.Rect(8*WINDOWWIDTH/10-40,8*WINDOWHEIGHT/10-30, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), ResetButton.clicked, self)
        button0 = TimeStepButton("time", "timestep_button.png", pygame.Rect(8*WINDOWWIDTH/10-40,7*WINDOWHEIGHT/10-40, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), TimeStepButton.clicked, self)
        button1 = RayButton("ray","ray.png",pygame.Rect(8.5*WINDOWWIDTH/10-30,WINDOWHEIGHT/10,WINDOWWIDTH/10,WINDOWHEIGHT/10),RayButton.clicked, self)
        button2 = SharkButton("shark","shark.png",pygame.Rect(8.5*WINDOWWIDTH/10-30,2*WINDOWHEIGHT/10 + 10,WINDOWWIDTH/10,WINDOWHEIGHT/10),SharkButton.clicked, self)
        button3 = ScallopButton("scallop", "scallop.png", pygame.Rect(8.5*WINDOWWIDTH/10-30,3*WINDOWHEIGHT/10 + 20, WINDOWWIDTH/10, WINDOWHEIGHT/10), ScallopButton.clicked, self)
        
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

        Screen.__init__(self, self.buttons, self.actors, "Background_modsim.png")


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


        self.rayOffset = 0
        self.sharkOffset = 0
        self.scallopOffset = 0

        self.rayX = 0
        self.sharkX = 0
        self.scallopX = 0
        self.win = 0

        self.howManyRays = 0
        self.howManySharks = 0
        self.howManyScallops = 0


        self.numrayLabel.updateText("Rays: " + str(self.howManyRays))
        self.changerayLabel.updateText("Change: " + str(0))
        self.numsharkLabel.updateText("Sharks: " + str(self.howManySharks))
        self.changesharkLabel.updateText("Change: " + str(0))
        self.numscallopLabel.updateText("Scallops: " + str(self.howManyScallops))
        self.changescallopLabel.updateText("Change: " + str(0))


        self.timesteps = 0
        self.timeLabel.updateText("Timestep: " + str(self.timesteps))
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


        rays_t_minus_1 = self.howManyRays
        sharks_t_minus_1 = self.howManySharks
        scallops_t_minus_1 = self.howManyScallops
        #plankton_t_minus_1 = self.howManyPlankton

        ############MODEL CONSTANTS############

        A0 = self.howManyScallops*5000
        R0 = self.howManyRays*5000
        S0 = self.howManySharks*5000



        ##############MODEL#####################


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


        self.howManyRays = int(R1/5000)
        self.howManySharks = int(S1/5000)
        self.howManyScallops = int(A1/5000)



        self.changeInRays = (self.howManyRays-rays_t_minus_1)
        self.changeInSharks = (self.howManySharks-sharks_t_minus_1)
        self.changeInScallops = (self.howManyScallops-scallops_t_minus_1)


        self.numrayLabel.updateText("Rays: " + str(self.howManyRays))
        self.changerayLabel.updateText("Change: " + str(self.changeInRays))
        self.numsharkLabel.updateText("Sharks: " + str(self.howManySharks))
        self.changesharkLabel.updateText("Change: " + str(self.changeInSharks))
        self.numscallopLabel.updateText("Scallops: " + str(self.howManyScallops))
        self.changescallopLabel.updateText("Change: " + str(self.changeInScallops))


        for i in range(1,self.howManyRays+1):
            
            if (i-1) %50 == 0:
                self.rayOffset = 0

            if i >200:
                print "no"
                break
            elif i >150:
                self.rayX = 30
                self.actors.append(Ray("rayA"+str(i), pygame.Rect(130,100+self.rayOffset,10,10), "ray.png", self))
            elif i>100:
                self.rayX = 20
                self.actors.append(Ray("rayA"+str(i), pygame.Rect(120,100+self.rayOffset,10,10), "ray.png", self))
            elif i > 50:
                self.rayX = 10
                self.actors.append(Ray("rayA"+str(i), pygame.Rect(110,100+self.rayOffset,10,10), "ray.png", self))

            elif i <=50:
                self.rayX = 0
                self.actors.append(Ray("rayA"+str(i), pygame.Rect(100,100+self.rayOffset,10,10), "ray.png", self))

            self.rayOffset += 10

        print 'rays ' + str(self.howManyRays)
        print 'Ray x ' + str(self.rayX)



        for i in range(1,self.howManySharks+1):

            if (i-1) %50 == 0:
                self.sharkOffset = 0

            if i >200:
                print "no"
                break
            elif i >150:
                self.sharkX = 30
                self.actors.append(Shark("sharkA"+str(i), pygame.Rect(360,100+self.sharkOffset,10,10), "shark.png", self))
            elif i>100:
                self.sharkX = 20
                self.actors.append(Shark("sharkA"+str(i), pygame.Rect(350,100+self.sharkOffset,10,10), "shark.png", self))
            elif i > 50:
                self.sharkX = 10
                self.actors.append(Shark("sharkA"+str(i), pygame.Rect(340,100+self.sharkOffset,10,10), "shark.png", self))

            elif i <=50:
                self.sharkX = 0
                self.actors.append(Shark("sharkA"+str(i), pygame.Rect(330,100+self.sharkOffset,10,10), "shark.png", self))

            self.sharkOffset += 10

        print 'sharks ' + str(self.howManySharks)



        for i in range(1,self.howManyScallops+1):
            if (i-1) %50 == 0:
                self.scallopOffset = 0

            if i >200:
                print "no"
                break
            elif i >150:
                self.scallopX = 30
                self.actors.append(Scallop("scallopA"+str(i), pygame.Rect(590,100+self.scallopOffset,10,10), "scallop.png", self))
            elif i>100:
                self.scallopX = 20
                self.actors.append(Scallop("scallopA"+str(i), pygame.Rect(580,100+self.scallopOffset,10,10), "scallop.png", self))
            elif i > 50:
                self.scallopX = 10
                self.actors.append(Scallop("scallopA"+str(i), pygame.Rect(570,100+self.scallopOffset,10,10), "scallop.png", self))

            elif i <=50:
                self.scallopX = 0
                self.actors.append(Scallop("scallopA"+str(i), pygame.Rect(560,100+self.scallopOffset,10,10), "scallop.png", self))

            self.scallopOffset += 10
            
        print 'scallops ' + str(self.howManyScallops)


        if abs(self.changeInRays) <=2:
            if abs(self.changeInSharks) <=2:
                if abs(self.changeInScallops) <=2:
                    self.win += 1
        if self.win >= 5:
            self.actors.append(self.winLabel)
            print "you win"


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


class GBackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
        #self.image.fill((0,0,255))
    def clicked(self, button_name):
        self.model.gamemodel.currentscreen = self.model.gamemodel.homescreen



class RayButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        #instantiate and put a ray on the gamescreen     
        self.model.howManyRays +=1    


        i = self.model.howManyRays
        if (i-1) %50 == 0:
            self.model.rayOffset = 0
        if i >200:                
            print "no"
        elif i >150:
            self.model.rayX = 30
            self.model.actors.append(Ray("rayA"+str(i), pygame.Rect(130,100+self.model.rayOffset,10,10), "ray.png", self.model))
        elif i>100:
            self.model.rayX = 20
            self.model.actors.append(Ray("rayA"+str(i), pygame.Rect(120,100+self.model.rayOffset,10,10), "ray.png", self.model))
        elif i > 50:
            self.model.rayX = 10
            self.model.actors.append(Ray("rayA"+str(i), pygame.Rect(110,100+self.model.rayOffset,10,10), "ray.png", self.model))

        elif i <=50:
            self.model.rayX = 0
            self.model.actors.append(Ray("rayA"+str(i), pygame.Rect(100,100+self.model.rayOffset,10,10), "ray.png", self.model))
            
        self.model.rayOffset += 10


        print 'rays ' + str(self.model.howManyRays)
        self.model.numrayLabel.updateText("Rays: " + str(self.model.howManyRays))
      


class SharkButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
        
    def clicked(self, button_name):
        self.model.howManySharks +=1  

        i = self.model.howManySharks
        if (i-1) %50 == 0:
            self.model.sharkOffset = 0
        if i >200:                
            print "no"
        elif i >150:
            self.model.sharkX = 30
            self.model.actors.append(Shark("sharkA"+str(i), pygame.Rect(360,100+self.model.sharkOffset,10,10), "shark.png", self.model))
        elif i>100:
            self.model.sharkX = 20
            self.model.actors.append(Shark("sharkA"+str(i), pygame.Rect(350,100+self.model.sharkOffset,10,10), "shark.png", self.model))
        elif i > 50:
            self.model.sharkX = 10
            self.model.actors.append(Shark("sharkA"+str(i), pygame.Rect(340,100+self.model.sharkOffset,10,10), "shark.png", self.model))

        elif i <=50:
            self.model.sharkX = 0
            self.model.actors.append(Shark("sharkA"+str(i), pygame.Rect(330,100+self.model.sharkOffset,10,10), "shark.png", self.model))
            
        self.model.sharkOffset += 10
        print 'sharks ' + str(self.model.howManySharks)
        self.model.numsharkLabel.updateText("Sharks: " + str(self.model.howManySharks))


class ScallopButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.transform.scale(pygame.image.load(im), (WINDOWWIDTH/10,WINDOWHEIGHT/10))
       
    def clicked(self, button_name):
        self.model.howManyScallops +=1 
     
        i = self.model.howManyScallops
        if (i-1) %50 == 0:
            self.model.scallopOffset = 0
        if i >200:                
            print "no"
        elif i >150:
            self.model.scallopX = 30
            self.model.actors.append(Scallop("scallopA"+str(i), pygame.Rect(590,100+self.model.scallopOffset,10,10), "scallop.png", self.model))
        elif i>100:
            self.model.scallopX = 20
            self.model.actors.append(Scallop("scallopA"+str(i), pygame.Rect(580,100+self.model.scallopOffset,10,10), "scallop.png", self.model))
        elif i > 50:
            self.model.scallopX = 10
            self.model.actors.append(Scallop("scallopA"+str(i), pygame.Rect(570,100+self.model.scallopOffset,10,10), "scallop.png", self.model))

        elif i <=50:
            self.model.scallopX = 0
            self.model.actors.append(Scallop("scallopA"+str(i), pygame.Rect(560,100+self.model.scallopOffset,10,10), "scallop.png", self.model))
            
        self.model.scallopOffset += 10
        print 'scallops ' + str(self.model.howManyScallops)
        self.model.numscallopLabel.updateText("Scallops: " + str(self.model.howManyScallops))




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
            self.model.numsharkLabel.updateText("Sharks: " + str(self.model.howManySharks))



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
            self.model.numscallopLabel.updateText("Scallops: " + str(self.model.howManyScallops))


 