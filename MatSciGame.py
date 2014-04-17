# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 12:23:07 2014

@author: ragspiano
"""

#!/usr/bin/python3

"""Square clicking using planes

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   Based on a pure PyGame implementation
"""

# This file is part of planes.
#
# planes is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# planes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with planes.  If not, see <http://www.gnu.org/licenses/>.

# work started on 03. Oct 2010

import sys

# Add current and parent directory. One of them is supposed to contain the
# planes package.
#
sys.path.append("../")
sys.path.append("./")

import pygame
from planes import *
import planes
from collections import deque
from screen import Screen
from screen import Button
from MatSciScreen import MixingScreen


WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class StartButton(Button):
	def __init__(self, label, im, rect, callback, model):
		Button.__init__(self, label, rect, callback, model)
		self.image = pygame.image.load(im)
	def clicked(self, button_name):
		self.model.currentscreen = self.model.startScreen

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

class Material(planes.Plane):

    def __init__(self, name = None, rect = None, draggable = True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.image.fill((255, 0, 0))

        self.position = rect.center
        self.Xpos = self.position[0]
        self.Ypos = self.position[1]
        self.name = name
        self.strength = 0
        self.meltingPoint = 0

    def clicked(self, button_name):
        self.image.fill((255,0,0))

class DropZone(planes.Plane):
    def __init__(self, name, rect, screen):

        self.name = name
        self.rect = rect
        self.Xpos = self.rect.x
        self.Ypos = self.rect.y

        self.screen = screen
        planes.Plane.__init__(self, name, rect, draggable = False, grab = True)
        self.image.fill((0,0,255))
        



class MatSciGame():
    def __init__(self):
        self.materials = []
        self.newMaterials = []
        self.actors = self.materials + self.newMaterials
        self.startScreen = MixingScreen(self)
        start = StartButton("start","startbut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),StartButton.clicked, self)
        settings = SettingsButton("settings","setbut.png",pygame.Rect(WINDOWWIDTH/8,6*WINDOWHEIGHT/8 + 30,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),SettingsButton.clicked, self)
        tutorial = TutorialButton("tutorial","tutbut.png",pygame.Rect(WINDOWWIDTH/8,5*WINDOWHEIGHT/8 + 20,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),TutorialButton.clicked, self)
        home = HomeButton("home","homebut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),HomeButton.clicked, self)
        tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)
        self.homescreen = Screen([start,settings,tutorial],[titleRect("home.png",tr,WHITE)],BLACK)
        self.settingsscreen = Screen([home,settings,tutorial],[titleRect("settings.png",tr,WHITE)],BLACK)
        self.tutorialscreen = Screen([home,settings, tutorial],[titleRect("tut.png",tr,WHITE)],BLACK)
    
        self.currentscreen = self.homescreen