import sys

# Add current and parent directory. One of them is supposed to contain the
# planes package.
#
sys.path.append("../")
sys.path.append("./")

import pygame
from planes import *
from collections import deque
from screen import Screen
from screen import Button
from screen import DropZone
from screen import ScreenText
import GameReal

import planes

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image.fill((0,0,255))
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.playScreen

class WrenchButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image.fill(GREEN)
        self.note = planes.Plane("Note1",pygame.Rect(rect.right,rect.bottom,200,200),False,False)
        self.note.image.fill(WHITE)
    def clicked(self, button_name):
        print "clicked wrench"
        names = [label.name for label in self.model.Notificationlabels]
        if self.note.name in names:
            index = names.index(self.note.name)
            del(self.model.actors[index])
        else:
            self.model.Notificationlabels.append(self.note)

class NutButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image.fill(GREEN)
        self.note = planes.Plane("Note1",pygame.Rect(rect.right,rect.bottom-300,200,200),False,False)
        self.note.image.fill(WHITE)
    def clicked(self, button_name):
        print "clicked nut"
        names = [label.name for label in self.model.Notificationlabels]
        if self.note.name in names:
            index = names.index(self.note.name)
            del(self.model.actors[index])
        else:
            self.model.Notificationlabels.append(self.note)

class HammerButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image.fill(GREEN)
        self.note = planes.Plane("Note1",pygame.Rect(rect.left,rect.bottom-350,200,200),False,False)
        self.note.image.fill(WHITE)
    def clicked(self, button_name):
        print "clicked hammer"
        names = [label.name for label in self.model.Notificationlabels]
        if self.note.name in names:
            index = names.index(self.note.name)
            del(self.model.actors[index])
        else:
            self.model.Notificationlabels.append(self.note)

class GearButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image.fill(GREEN)
        self.note = planes.Plane("Note1",pygame.Rect(rect.left-100,rect.bottom-300,200,200),False,False)
        self.note.image.fill(WHITE)
    def clicked(self, button_name):
        print "clicked gear"
        names = [label.name for label in self.model.Notificationlabels]
        if self.note.name in names:
            index = names.index(self.note.name)
            del(self.model.actors[index])
        else:
            self.model.Notificationlabels.append(self.note)

class NailButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image.fill(GREEN)
        self.note = planes.Plane("Note1",pygame.Rect(rect.left-100,rect.bottom,200,200),False,False)
        self.note.image.fill(WHITE)
    def clicked(self, button_name):
        print "clicked nail"
        names = [label.name for label in self.model.Notificationlabels]
        if self.note.name in names:
            index = names.index(self.note.name)
            del(self.model.actors[index])
        else:
            self.model.Notificationlabels.append(self.note)



class infoScreen(Screen):
    def __init__(self, tools, parts, game):
        self.tools = tools
        self.parts = parts
        self.game = game

        self.Notificationlabels = []
        back = BackButton("BackButton", BLUE, pygame.Rect(0, WINDOWHEIGHT-100, 200, 100), BackButton.clicked, self)
        wrench = WrenchButton("WrenchButton",GREEN,pygame.Rect(100,100,100,100), WrenchButton.clicked,self)
        nut = NutButton("NutButton",GREEN,pygame.Rect(100,WINDOWHEIGHT-300,100,100), NutButton.clicked,self)
        hammer = HammerButton("HammerButton",GREEN,pygame.Rect(500,WINDOWHEIGHT-300,100,100), HammerButton.clicked,self)
        gear = GearButton("GearButton",GREEN,pygame.Rect(1000,WINDOWHEIGHT-300,100,100), GearButton.clicked,self)
        nail = NailButton("NailButton",GREEN,pygame.Rect(1000,100,100,100), NailButton.clicked,self)
        self.actors = self.Notificationlabels
        buttons = [back,wrench,nut,hammer,gear,nail]
        
        Screen.__init__(self,buttons,self.actors,BLACK)
    def update(self):
        self.actors = self.Notificationlabels