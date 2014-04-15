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

WINDOWWIDTH = 800
WINDOWHEIGHT = 800

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Upgrade(planes.Plane):
    def __init__(self, name, rect, im, cost, draggable=True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.cost = cost
        self.image.fill(im)

    def clicked(self, button_name):
        self.image.fill((255,0,0))

    def applyUpgrade(self, robot):
        pass

class BuildButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.buildscreen

class StoreScreen(Screen):
    def __init__(self, robot, game):
        self.robot = robot
        self.game = game
        start = BuildButton("tobuildscreen", pygame.Rect(WINDOWWIDTH-75, WINDOWHEIGHT-50, 75, 50), BuildButton.clicked, self)
        upgrade1 = Upgrade("u1", pygame.Rect(0,0,50,50), BLUE, 20)
        upgrade2 = Upgrade("u2", pygame.Rect(70,0,50,50), GREEN, 20)
        upgrade3 = Upgrade("u3", pygame.Rect(140,0,50,50), WHITE, 20)
        self.shoppingcart = DropZone("shoppingcart", pygame.Rect(200,200,200,200))
        buttons = [start]
        self.actors = [upgrade1, upgrade2, upgrade3, self.shoppingcart]
        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        pass


