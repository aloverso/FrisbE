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
import time
from screen import ScreenText

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

class Upgrade(planes.Plane):
    def __init__(self, name, rect, im, cost, value, draggable=True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.Xpos = rect.x
        self.Ypos = rect.y
        self.cost = cost
        self.image.fill(im)
        self.value = value
        self.width = rect.width
        self.height = rect.height
        self.origRect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)

    def clicked(self, button_name):
        self.image.fill((255,0,0))

class MotorUpgrade(Upgrade):
    def __init__(self, name, rect, im, cost, value):
        Upgrade.__init__(self, name, rect, im, cost, value)

class BumperUpgrade(Upgrade):
    def __init__(self, name, rect, im, cost, value):
        Upgrade.__init__(self, name, rect, im, cost, value)

class BuildButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.buildscreen

class BuyButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        lis = self.model.shoppingcart.thingsDroppedOnMe
        for i in range(len(lis)):
            upgrade = lis[i]
            if isinstance(upgrade, MotorUpgrade):
                self.model.game.purchases.append(MotorUpgrade("b"+str(pygame.time.get_ticks()), upgrade.origRect, GREEN, upgrade.cost, upgrade.value))
            if isinstance(upgrade, BumperUpgrade):
                self.model.game.purchases.append(BumperUpgrade("b"+str(pygame.time.get_ticks()), upgrade.origRect, GREEN, upgrade.cost, upgrade.value))
            time.sleep(.01)
        for upgrade in lis:
            names = [actor.name for actor in self.model.actors]
            if upgrade.name in names:
                index = names.index(upgrade.name)
                del(self.model.actors[index])


class StoreScreen(Screen):
    def __init__(self, robot, game):
        self.robot = robot
        self.game = game
        self.startPosition = (400,400)
        start = BuildButton("tobuildscreen", pygame.Rect(scrright-75, scrbottom-50, 75, 50), BuildButton.clicked, self)
        buy = BuyButton("buythings", pygame.Rect(400, scrbottom-75, 100,75), BuyButton.clicked, self)
        font1 = pygame.font.SysFont("Arial", 40)
        motorLabel = ScreenText("motorLabel", "Motor Upgrades", pygame.Rect(scrleft,scrtop, 170, 50), font1)
        mu1 = MotorUpgrade("mu1", pygame.Rect(scrleft,scrtop+60,50,50), BLUE, 20, 0.3)
        mu2 = MotorUpgrade("mu2", pygame.Rect(scrleft+60,scrtop+60,50,50), BLUE, 40, 0.2)
        mu3 = MotorUpgrade("mu3", pygame.Rect(scrleft+120,scrtop+60,50,50), BLUE, 60, 0.1)
        self.shoppingcart = DropZone("shoppingcart", pygame.Rect(350,50,800,600))
        self.shoppingcart.image = pygame.image.load("shoppingcart.png")


        bumperLabel = ScreenText("bumperLabel", "Bumper Upgrades", pygame.Rect(scrleft, mu3.rect.bottom + 30, 170, 50), font1)
        bu1 = BumperUpgrade("bu1", pygame.Rect(scrleft, bumperLabel.rect.bottom + 10, 50, 50), BLUE, 20, 7)
        bu2 = BumperUpgrade("bu2", pygame.Rect(scrleft+60, bumperLabel.rect.bottom + 10, 50, 50), BLUE, 40, 5)
        bu3 = BumperUpgrade("bu3", pygame.Rect(scrleft+120, bumperLabel.rect.bottom + 10, 50, 50), BLUE, 60, 3)


        buttons = [start, buy]
        self.upgrades = [mu1, mu2, mu3, bu1, bu2, bu3]
        self.actors = [self.shoppingcart, motorLabel, bumperLabel] + self.upgrades
        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        pass
