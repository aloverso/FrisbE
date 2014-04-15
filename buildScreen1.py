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


class StartButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.movescreen


class AddButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        self.model.actors.append(Upgrade("u2", pygame.Rect(60,60,50,50), BLUE, 20))


class StoreButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.storescreen

class BuildScreen(Screen):
    def __init__(self, robot, game):
        self.robot = robot
        self.game = game
        store = StoreButton("storebutton", pygame.Rect(0, WINDOWHEIGHT-50, 75, 50), StoreButton.clicked, self)
        start = StartButton("movescreen", pygame.Rect(WINDOWWIDTH-75, WINDOWHEIGHT-50, 75, 50), StartButton.clicked, self)
        add = AddButton("add", pygame.Rect(500, 0, 75, 50), AddButton.clicked, self)
        upgrade1 = Upgrade("u1", pygame.Rect(0,0,50,50), BLUE, 20)
        buttons = [start, store, add]
        self.actors = [robot,upgrade1]
        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        pass

