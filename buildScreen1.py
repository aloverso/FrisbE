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
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.movescreen
        self.model.robot.setPosition(self.model.game.movescreen.startPosition[0], self.model.game.movescreen.startPosition[1])

class StoreButton(Button):
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.storescreen
        self.model.robot.setPosition(self.model.game.storescreen.startPosition[0], self.model.game.storescreen.startPosition[1])

class UpgradeZone(DropZone):
    def __init__(self, name, rect, robot):
        DropZone.__init__(self,name,rect)
        self.robot = robot
    def dropped_upon(self, plane, coordinates):
        planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))
        plane.moving = False
        self.robot.money -= plane.cost
        self.robot.upgrades.append(plane)
        if isinstance(plane, storeScreen1.MotorUpgrade):
            self.robot.motorspeed = plane.value
        if isinstance(plane, storeScreen1.BumperUpgrade):
            self.robot.bumper = plane.value
        time.sleep(.5)
        plane.rect = plane.origRect


class BuildScreen(Screen):
    def __init__(self, robot, game):
        self.robot = robot
        self.startPosition = (400,400)
        self.game = game
        self.upgradezone = UpgradeZone("upgradezone", pygame.Rect(200,200,300,300), self.robot)
        store = StoreButton("storebutton", pygame.Rect(scrleft, scrbottom-50, 75, 50), StoreButton.clicked, self)
        start = StartButton("movescreen", pygame.Rect(scrright-75, scrbottom-50, 75, 50), StartButton.clicked, self)
        buttons = [start, store]
        font1 = pygame.font.SysFont("Arial", 40)
        self.motorLabel = planes.Plane("motorLabel", pygame.Rect(scrleft,scrtop,170,50), draggable=False, grab=False)
        self.motorLabel.image = pygame.image.load("motorupgrade_label.png")
        #self.motorLabel = ScreenText("motorLabel", "Motor Upgrades", pygame.Rect(scrleft,scrtop, 170, 50), font1)
        self.bumperLabel = ScreenText("bumperLabel", "Bumper Upgrades", pygame.Rect(scrleft, scrtop+60+50 + 30, 170, 50), font1)


        self.actors = [self.upgradezone, self.motorLabel, self.bumperLabel] + self.game.purchases
        self.startPosition = (200,200)
        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        self.actors = [self.upgradezone, self.motorLabel, self.bumperLabel] + self.game.purchases
