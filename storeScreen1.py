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

MOVEBUTTON_HEIGHT = 75
MOVEBUTTON_WIDTH = 50

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

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

    def clicked(self, button_name):
        self.image.fill((255,0,0))

class MotorUpgrade(Upgrade):
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
        for upgrade in self.model.shoppingcart.thingsDroppedOnMe:
            self.model.game.purchases.append(upgrade)
        print "bought the items"
        print self.model.game.purchases

class StoreScreen(Screen):
    def __init__(self, robot, game):
        self.robot = robot
        self.game = game
        self.startPosition = (400,400)
        start = BuildButton("tobuildscreen", pygame.Rect(WINDOWWIDTH-75, WINDOWHEIGHT-50, 75, 50), BuildButton.clicked, self)
        buy = BuyButton("buythings", pygame.Rect(WINDOWWIDTH-100, 0, 100,75), BuyButton.clicked, self)
        self.upgrade1 = MotorUpgrade("u1", pygame.Rect(0,0,50,50), BLUE, 20, 0.3)
        self.upgrade2 = MotorUpgrade("u2", pygame.Rect(70,0,50,50), GREEN, 30, 0.2)
        self.upgrade3 = MotorUpgrade("u3", pygame.Rect(140,0,50,50), WHITE, 40, 0.1)
        self.shoppingcart = DropZone("shoppingcart", pygame.Rect(200,200,200,200))
        buttons = [start, buy]
        self.upgrades = [self.upgrade1,self.upgrade2,self.upgrade3]
        self.actors = [self.shoppingcart] + self.upgrades
        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        pass

"""
why does the remove function throw an error?

"""
