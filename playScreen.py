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
        if self.screen.game.level == 0:
            requiredTool = "Wrench"
            requiredPart = "Gear"
        if self.screen.game.level == 1:
            requiredTool = "Hammer"
            requiredPart = "Nail"
        if self.screen.game.level == 2:
            requiredTool = "Wrench"
            requiredPart = "Nut"

       

        if len(self.thingsDropped) == 2:
            if self.thingsDropped[0].name == requiredPart or self.thingsDropped[0].name == requiredTool:
                if self.thingsDropped[1].name == requiredPart or self.thingsDropped[1].name == requiredTool:
                    font1 = pygame.font.SysFont("Arial", 20)
                    repaired = ScreenText("text1", "object repaired", pygame.Rect(100, 3*WINDOWHEIGHT/4, 200, 50), font1)
                    self.screen.Notificationlabels.append(repaired)
                    self.screen.creationTime = pygame.time.get_ticks()
                    self.screen.game.level+=1

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
        self.image = pygame.image.load(im)
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
        self.TargetArea = TargetZone("TargetZone",pygame.Rect(400,175,400,400),self)
        if self.game.level == 0:
            self.TargetArea.image = pygame.image.load()
        if self.game.level == 1:
            self.TargetArea.image = pygame.image.load()
        if self.game.level == 2:
            self.TargetArea.image = pygame.image.load()
        self.Notificationlabels = []
        self.creationTime = 0



        info = infoScreenButton("infobutton", "i_small.png", pygame.Rect(WINDOWWIDTH-100, 0, 100, 100), infoScreenButton.clicked, self)
        back = BackButton("BackButton", "back_button_med.png", pygame.Rect(0, WINDOWHEIGHT-100, 200, 100), BackButton.clicked, self)
        buttons = [info,back]

        
        self.actors = [self.TargetArea] + self.parts + self.tools + self.Notificationlabels

        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        self.actors = [self.TargetArea] + self.parts + self.tools + self.Notificationlabels
        if len(self.Notificationlabels) > 0:
            time = pygame.time.get_ticks()
            if (self.creationTime > 0) and (time - self.creationTime < 2000):
                pass
            else:
                self.creationTime = 0
                self.Notificationlabels = []
                self.actors = [self.TargetArea] + self.parts + self.tools + self.Notificationlabels
        else:
            self.actors = [self.TargetArea] + self.parts + self.tools + self.Notificationlabels