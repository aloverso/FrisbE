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


class TargetZone(DropZone):
    def __init__(self,name,rect,screen):
        DropZone.__init__(self, name, rect)
        self.screen = screen
        
        self.firstDropped = None
        self.firstDroppedCoordinates = None
        
        self.secondDropped = None
        self.secondDroppedCoordinates = None
        self.thingsDropped = []
        
    def dropped_upon(self, plane, coordinates):

        self.thingsDropped.append(plane)
        planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))

        requiredTool = "Wrench"
        requiredPart = "Gear"

       

        if len(self.thingsDropped) >= 2:
            for things in self.thingsDropped:
                if plane.name == requiredPart and plane.name ==requiredTool:
                    things += 1
            font1 = pygame.font.SysFont("Arial", 20)
            repaired = ScreenText("text1", "object repaired", pygame.Rect(100, 3*WINDOWHEIGHT/4, 200, 50), font1)
            
            names = [label.name for label in self.screen.Notificationlabels]
            if repaired.name in names:
                index = names.index(repaired.name)
                del(self.screen.Notificationlabels[index])
            else:
                self.screen.Notificationlabels.append(repaired)


class infoScreenButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        if isinstance(im, str):
            self.image = pygame.image.load(im)
        else:
            self.image.fill(im)
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.infoScreen

class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image.fill((0,0,255))
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.homescreen 

        
class titleRect(planes.Plane):
	def __init__(self, im, rect, color):
		planes.Plane.__init__(self,"title",rect,draggable=False, grab=False)
		self.image.fill(color)
		self.rect = rect
		self.color = color
		self.image = pygame.image.load(im)




#Stuff I need for my game: Tools, Parts, Target Location, False Target, garage, tool box




class playScreen(Screen):
    def __init__(self, tools, parts, game):
        self.tools = tools
        self.parts = parts
        self.game = game
        self.TargetArea = TargetZone("TargetZone",pygame.Rect(410,70,360,590),self)
        self.Notificationlabels = []



        info = infoScreenButton("infobutton", WHITE, pygame.Rect(WINDOWWIDTH-100, 0, 75, 50), infoScreenButton.clicked, self)
        back = BackButton("BackButton", BLUE, pygame.Rect(0, WINDOWHEIGHT-100, 200, 100), BackButton.clicked, self)
        buttons = [info,back]

        
        self.actors = [self.TargetArea] + self.parts + self.tools + self.Notificationlabels

        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        self.actors = [self.TargetArea] + self.parts + self.tools + self.Notificationlabels
