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
import MatSciGame
import planes

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class TargetZone(DropZone):
    def __init__(self,name,rect,screen, model):
        DropZone.__init__(self, name, rect)
        self.screen = screen
        self.model = model
        
        self.firstDropped = None
        self.firstDroppedCoordinates = None
        
        self.secondDropped = None
        self.secondDroppedCoordinates = None
        self.thingsDropped = 0
        self.creationTime = 0
        
    def dropped_upon(self, plane, coordinates):

       self.thingsDropped +=1
       planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))
       
       if self.thingsDropped == requiredTool:
           
           self.firstDropped = plane
           self.firstDroppedCoordinates = coordinates
           
       
       if self.thingsDropped == requiredPart:
           self.secondDropped = plane
           font1 = pygame.font.SysFont("Arial", 60)
           self.screen.Notificationlabels.append(ScreenText("text1", "object repaired", pygame.Rect(100, 3*WINDOWHEIGHT/4, 200, 50), font1))
           self.level = level + 1
      
           
           self.screen.actors =  self.screen.dropZones + self.screen.materials + self.screen.newMaterials + self.screen.Notificationlabels
                          
                      
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

class playScreen(Screen):
    def __init__(self, game, tools, parts):
        self.game = game
        self.tools = tools
        self.parts = parts
        

        Screen.__init__(self, self.buttons, self.actors, (0,128,0))
    
    def update(self):
        pass

class infoScreen(Screen):
    def __init__(self, game, tools, parts):
        self.game = game
        self.tools = tools
        self.parts = parts
        self.database = database

    def toolClicked(self,tools,parts):
        self.tools.database = database
        self.screen.Notificationlabels.append(ScreenText("text1", database, pygame.Rect(100, 3*WINDOWHEIGHT/4, 200, 50), font1))
        passn


        Screen.__init__(self, self.buttons, self.actors, (128,0,0))


