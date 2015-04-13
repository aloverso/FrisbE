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
from screen import ScreenText
from MatSciScreen import MixingScreen
from MatSciScreen import ForceTestScreen
from MatSciScreen import MeltingTestScreen
from MatSciScreen import ItemMakeScreen
from MatSciScreen import ItemViewScreen


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

class ForceScreenButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.forceScreen

class MixScreenButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.startScreen

class HeatScreenButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.heatScreen
        
class ItemScreenButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.itemScreen

class ItemViewScreenButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.currentscreen = self.model.itemViewScreen
        
class titleRect(planes.Plane):
	def __init__(self, im, rect, color):
		planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
		self.image.fill(color)
		self.rect = rect
		self.color = color
		self.image = pygame.image.load(im)

class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.toDash = True


#Stuff I need for my game: materials

class Material(planes.Plane):
    def __init__(self, name, strength, strengthTested, meltingPoint, meltingPointTested, appearence, tier, rect, screen, draggable = True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        

        self.position = rect.center
        self.Xpos = self.position[0]
        self.Ypos = self.position[1]
        
        self.name = name
        self.strength = strength
        self.meltingPoint = meltingPoint
        self.appearence = appearence
        self.tier = tier
        
        if self.tier == 1:
            self.image = pygame.image.load("img/materialT0.png")
        
        if self.tier == 2:
            self.image = pygame.image.load("img/materialT1.png")
        
        if self.tier == 3:
            self.image = pygame.image.load("img/materialT2.png")
        
        if self.tier >= 4:
            self.image = pygame.image.load("img/materialT3.png")
        
#        self.red = color[0]
#        self.green = color[1]
#        self.blue = color[2]
        
        self.strengthTested = strengthTested
        self.meltingPointTested = meltingPointTested 
        
        self.screen = screen

    def clicked(self, button_name):
        pass
    
    def mouseover_callback(self):
        if self.meltingPointTested == True:
            printMelting = str(self.meltingPoint)
        else:
            printMelting = "?"
        
        if self.strengthTested == True:
            printStrength = str(self.strength)
        else:
            printStrength = "?"
        
        self.screen.currentscreen.infoLabels.append(ScreenText("infoText" + str(self.strength), "Strength = " + str(printStrength) + " Melting Point = " + str(printMelting) + " Appearence = " + str(self.appearence), pygame.Rect(self.Xpos + 20, self.Ypos, 350, 50), pygame.font.SysFont("Arial", 14)))        
        self.screen.currentscreen.actors =  self.screen.currentscreen.actors + self.screen.currentscreen.infoLabels
     
    def mouseout_callback(self):
        self.screen.currentscreen.infoLabels = []
        self.screen.currentscreen.actors =  self.screen.currentscreen.dropZones + self.screen.currentscreen.materials + self.screen.currentscreen.newMaterials + self.screen.currentscreen.constantLabels 
        
class Item(planes.Plane):
    def __init__(self, name, rect, bestStrength, bestMeltingPoint, appearenceNeed, strengthImport, meltImport, appearImport,color, material = None, draggable = True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        
        self.image.fill(color)

        self.position = rect.center
        self.Xpos = self.position[0]
        self.Ypos = self.position[1]
        self.name = name
        self.material = material
        self.bestStrength = bestStrength
        self.bestMeltingPoint = bestMeltingPoint
        self.appearenceNeed = appearenceNeed
        self.strengthImport = strengthImport
        self.meltImport = meltImport
        self.appearImport = appearImport
        
        if self.name == "cup":
            self.image = pygame.image.load("img/CupItem.png")
        if self.name == "poker":
            self.image = pygame.image.load("img/PokerItem.png")
        if self.name == "hammer":
            self.image = pygame.image.load("img/HammerItem.png")
        if self.name == "table":
            self.image = pygame.image.load("img/TableItem.png")
        if self.name == "decor":
            self.image = pygame.image.load("img/DecorItem.png")

class CreatedItem(planes.Plane):
    def __init__(self, name, color, strength, meltingPoint, appearence, material, money, screen):
        
        
        self.meltingPoint = meltingPoint
        self.strength = strength
        self.appearence = appearence
        self.money = money
        self.name = name 
        
        self.rect = pygame.Rect(0,0,100,100)
        self.position = self.rect.center
        self.Xpos = self.position[0]
        self.Ypos = self.position[1]
        self.screen = screen
        
        planes.Plane.__init__(self, self.name, self.rect, draggable = False, grab = True)
                
        if self.name == "cup":
            self.image = pygame.image.load("img/CupItem.png")
        if self.name == "poker":
            self.image = pygame.image.load("img/PokerItem.png")
        if self.name == "hammer":
            self.image = pygame.image.load("img/HammerItem.png")
        if self.name == "table":
            self.image = pygame.image.load("img/TableItem.png")
        if self.name == "decor":
            self.image = pygame.image.load("img/DecorItem.png")  

        
    def setRect(self, rect):
        self.rect = rect
    def setName(self, name):
        self.name = name
    
    def mouseover_callback(self):
        self.screen.currentscreen.infoLabels.append(ScreenText("infoText2" + str(self.strength), "Strength = " + str(self.strength) + " Melting Point = " + str(self.meltingPoint) + " Appearence = " + str(self.appearence) + " Money = " + str(self.money), pygame.Rect(self.Xpos + 20, self.Ypos, 500, 50), pygame.font.SysFont("Arial", 40)))        
        self.screen.currentscreen.actors =  self.screen.currentscreen.actors + self.screen.currentscreen.infoLabels

    
    def mouseout_callback(self):
        self.screen.currentscreen.infoLabels = []
        self.screen.currentscreen.actors = self.screen.currentscreen.constantLabels + self.screen.currentscreen.shownItems
            
        
class MatSciGame():
    def __init__(self):
        self.materials = []
        self.newMaterials = []
        self.createdItems = []
        self.money = 10000        
        
        self.actors = self.materials + self.newMaterials
        self.clock = pygame.time.Clock()
        self.toDash = False
        
        self.startScreen = MixingScreen(self, self.materials, self.newMaterials, self.money)
        self.forceScreen = ForceTestScreen(self, self.materials, self.newMaterials, self.money)
        self.heatScreen = MeltingTestScreen(self, self.materials, self.newMaterials, self.money)
        self.itemScreen = ItemMakeScreen(self, self.materials, self.newMaterials, self.money)
        self.itemViewScreen = ItemViewScreen(self, self.materials, self.newMaterials, self.money)
        
        self.topCups = []
        self.topTables = []
        self.topPokers = []
        self.topDecors = []
        self.topHammers = []

        back = BackButton("back", "img/back_button_long.png", pygame.Rect(50,650,500,50), BackButton.clicked, self)

        start = StartButton("start","img/start_button.png",pygame.Rect(650,50,500,300),StartButton.clicked, self)
        tutorial = TutorialButton("tutorial","img/tutorial_button.png",pygame.Rect(650, 400, 500, 300),TutorialButton.clicked, self)
        home = HomeButton("home","img/title_button.png",pygame.Rect(650,50,500,300),HomeButton.clicked, self)
        tr = pygame.Rect(50, 50, 500, 575)
        self.homescreen = Screen([start,tutorial, back],[titleRect("img/matsci_logo.png",tr,WHITE)],BLACK)

        self.tutorialscreen = Screen([home, tutorial],[titleRect("img/robo_tutorial.png",tr,WHITE)],BLACK)

        self.currentscreen = self.homescreen