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
import planes
from collections import deque
from screen import Screen
from screen import Button
from screen import DropZone
from screen import ScreenText
import time
import storeScreen1
from moveScreen4 import MoveScreen


MOVEBUTTON_HEIGHT = 75
MOVEBUTTON_WIDTH = 50

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

class StartButton(Button):
    def __init__(self, label, rect, im, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.game.movescreen = MoveScreen(self.model.robot, self.model.game)
        self.model.game.currentscreen = self.model.game.movescreen
        self.model.robot.setPosition(self.model.game.movescreen.startPosition[0], self.model.game.movescreen.startPosition[1])

class StoreButton(Button):
    def __init__(self, label, rect, im, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.storescreen
        self.model.robot.setPosition(self.model.game.storescreen.startPosition[0], self.model.game.storescreen.startPosition[1])

class BackButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("img/back_button_med.png")
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.homescreen

class DefaultButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("img/default_button.png")
    def clicked(self, button_name):
        self.model.robot.motorspeed = self.model.robot.defaultMotorspeed
        self.model.robot.bumper = self.model.robot.defaultBumper
        for i in range(len(self.model.motorUpgradeIndicators)):
            if i == 0:
                self.model.motorUpgradeIndicators[i].on()
            else:
                self.model.motorUpgradeIndicators[i].off()
        for i in range(len(self.model.bumperUpgradeIndicators)):
            if i == 0:
                self.model.bumperUpgradeIndicators[i].on()
            else:
                self.model.bumperUpgradeIndicators[i].off()

class UpgradeZone(DropZone):
    def __init__(self, name, rect, robot, model):
        DropZone.__init__(self,name,rect)
        self.robot = robot
        self.model = model
        self.image = pygame.image.load("img/robot.png")
    def dropped_upon(self, plane, coordinates):
        planes.Plane.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))
        plane.moving = False
        self.robot.upgrades.append(plane)
        if isinstance(plane, storeScreen1.MotorUpgrade):
            self.robot.motorspeed = plane.value
            for i in range(len(self.model.motorUpgradeIndicators)):
                if i == plane.order:
                    self.model.motorUpgradeIndicators[i].on()
                else:
                    self.model.motorUpgradeIndicators[i].off()
        if isinstance(plane, storeScreen1.BumperUpgrade):
            self.robot.bumper = plane.value
            for i in range(len(self.model.bumperUpgradeIndicators)):
                if i == plane.order:
                    self.model.bumperUpgradeIndicators[i].on()
                else:
                    self.model.bumperUpgradeIndicators[i].off()

class UpgradeIndicator(planes.Plane):
    def __init__(self,name,rect):
        planes.Plane.__init__(self, name, rect, draggable=False, grab = False)
        self.isOn = False
        self.onImage = (255,255,255)
        self.offImage = (100,100,100)
    def on(self):
        self.isOn = True
        self.image.fill(self.onImage)
    def off(self):
        self.isOn = False
        self.image.fill(self.offImage)


class BuildScreen(Screen):
    def __init__(self, robot, game):
        self.robot = robot
        self.startPosition = (400,400)
        self.game = game
        self.upgradezone = UpgradeZone("upgradezone", pygame.Rect(410,70,360,590), self.robot, self)
        store = StoreButton("storebutton", pygame.Rect(scrleft, scrbottom-100, 200, 100), "img/store_button.png", StoreButton.clicked, self)
        start = StartButton("movescreen", pygame.Rect(scrright-200, scrbottom-100, 200, 100), "img/start_game_button.png", StartButton.clicked, self)
        back = BackButton("backbutton", pygame.Rect(WINDOWWIDTH-225, 60, 200, 50), BackButton.clicked, self)
        defaultbutt = DefaultButton("defaultbutton", pygame.Rect(WINDOWWIDTH-225, 500, 200, 50), DefaultButton.clicked, self)
        buttons = [start, store, back, defaultbutt]

        font0 = pygame.font.SysFont("Arial", 18)
        self.motorLevelLabel = ScreenText("mll", "Motor Upgrade Level", pygame.Rect(950, 210, 200, 50), font0)
        self.motorUpgradeIndicators = [UpgradeIndicator("m0", pygame.Rect(1000, 250, 20, 20)), UpgradeIndicator("m1", pygame.Rect(1030, 250, 20, 20)), UpgradeIndicator("m2", pygame.Rect(1060, 250, 20, 20)), UpgradeIndicator("m3", pygame.Rect(1090, 250, 20, 20))]
        for i in range(len(self.motorUpgradeIndicators)):
            if i == 0:
                self.motorUpgradeIndicators[i].on()
            else:
                self.motorUpgradeIndicators[i].off()

        self.bumperLevelLabel = ScreenText("bll", "Bumper Upgrade Level", pygame.Rect(950, 280, 200, 50), font0)
        self.bumperUpgradeIndicators = [UpgradeIndicator("b0", pygame.Rect(1000, 320, 20, 20)), UpgradeIndicator("b1", pygame.Rect(1030, 320, 20, 20)), UpgradeIndicator("b2", pygame.Rect(1060, 320, 20, 20)), UpgradeIndicator("b3", pygame.Rect(1090, 320, 20, 20))]
        for i in range(len(self.bumperUpgradeIndicators)):
            if i == 0:
                self.bumperUpgradeIndicators[i].on()
            else:
                self.bumperUpgradeIndicators[i].off()  

        font1 = pygame.font.SysFont("Arial", 40)
        self.moneyLabel = ScreenText("moneytext", "Money: "+str(self.robot.money), pygame.Rect(WINDOWWIDTH-225, 0, 200, 50), font1)
        self.motorLabel = planes.Plane("motorLabel", pygame.Rect(scrleft,scrtop,170,50), draggable=False, grab=False)
        self.motorLabel.image = pygame.image.load("img/motorupgrade_label.png")
        self.bumperLabel = planes.Plane("bumperLabel", pygame.Rect(scrleft, scrtop+60+50 + 30, 170, 50), draggable=False, grab=False)
        self.bumperLabel.image = pygame.image.load("img/bumperupgrade_label.png")
        self.labels = [self.motorLabel, self.bumperLabel, self.moneyLabel, self.motorLevelLabel, self.bumperLevelLabel]
        self.actors = [self.upgradezone] + self.labels + self.game.purchases + self.motorUpgradeIndicators + self.bumperUpgradeIndicators
        self.startPosition = (200,200)
        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        self.actors = [self.upgradezone] + self.labels + self.game.purchases + self.motorUpgradeIndicators + self.bumperUpgradeIndicators
        self.moneyLabel.updateText("Money: "+str(self.robot.money))