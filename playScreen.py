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
            self.screen.Notificationlabels.append(ScreenText("text1", "object repaired", pygame.Rect(100, 3*WINDOWHEIGHT/4, 200, 50), font1))

class Toolbox(DropZone):
    def __init__(self,name,rect,screen):
        DropZone.__init__(self, name, rect)
        self.image.fill((128,0,0))
        self.screen = screen
        self.coordinates = rect.center
        
        self.Xpos = self.coordinates[0]
        self.Ypos = self.coordinates[1]
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))

class Garage(DropZone):
    def __init__(self,name,rect,screen):
        DropZone.__init__(self, name, rect)
        self.image.fill((128,0,0))
        self.screen = screen
        self.coordinates = rect.center
        
        self.Xpos = self.coordinates[0]
        self.Ypos = self.coordinates[1]
        
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))

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



        info = infoScreenButton("infobutton", WHITE, pygame.Rect(0, WINDOWHEIGHT-50, 75, 50), infoScreenButton.clicked, self)
        back = BackButton("BackButton", BLUE, pygame.Rect(200, WINDOWHEIGHT-50, 75, 50), BackButton.clicked, self)
        buttons = [info,back]

        self.tools.append(GameReal.Tools("Hammer",1,pygame.Rect(500,0,20,20),WHITE))
        self.tools.append(GameReal.Tools("Wrench",2,pygame.Rect(500,1*WINDOWHEIGHT/5,20,20),BLUE))
        self.parts.append(GameReal.Parts("Gear",5,pygame.Rect(50,0,20,20),GREEN))
        self.parts.append(GameReal.Parts("Nut",6,pygame.Rect(50,WINDOWHEIGHT/5,20,20),WHITE))
        self.parts.append(GameReal.Parts("Nail",7,pygame.Rect(50,2*WINDOWHEIGHT/5,20,20),BLUE))
        self.actors = [self.TargetArea] + self.parts + self.tools + self.Notificationlabels

        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        self.actors = [self.TargetArea] + self.parts + self.tools + self.Notificationlabels
