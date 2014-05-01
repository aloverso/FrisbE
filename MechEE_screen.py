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

class MixZone(DropZone):
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
       
       if self.thingsDropped == 1:
           
           self.firstDropped = plane
           self.firstDroppedCoordinates = coordinates
           
       
       if self.thingsDropped == 2:
           self.secondDropped = plane
           self.secondDroppedCoordinates = coordinates
           font1 = pygame.font.SysFont("Arial", 60)
           self.screen.Notificationlabels.append(ScreenText("text1", "Made a New Material", pygame.Rect(100, 3*WINDOWHEIGHT/4, 200, 50), font1))
           
           newStrength = 0.5*self.firstDropped.strength + 0.5*self.secondDropped.strength
           newMeltingPoint = 0.5*self.firstDropped.meltingPoint + 0.5*self.secondDropped.meltingPoint
           
           if len(self.screen.newMaterials) < 10:
               self.screen.newMaterials.append((MatSciGame.Material("Newmat"+`len(self.screen.newMaterials)`, newStrength, newMeltingPoint, pygame.Rect((30, (len(self.screen.newMaterials)+1)*60, 20, 20)))))
           else:
               self.screen.newMaterials.append((MatSciGame.Material("Newmat"+`len(self.screen.newMaterials)`, newStrength, newMeltingPoint, pygame.Rect((60, (len(self.screen.newMaterials)+1-10)*60, 20, 20)))))
           
           planes.Plane.dropped_upon(self.screen.dropMats, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
           planes.Plane.dropped_upon(self.screen.dropMats, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
           
           print self.firstDropped.Xpos + self.screen.dropMats.Xpos
           print self.secondDropped.Xpos + self.screen.dropMats.Xpos
           
           self.screen.actors =  self.screen.dropZones + self.screen.materials + self.screen.newMaterials + self.screen.Notificationlabels
           
           self.thingsDropped = 0
           
           self.creationTime = pygame.time.get_ticks()
                             
    def getFirstTick(self):
        self.firstTick = self.model.clock.tick()
        return self.firstTick               
                      
class HoldZone(DropZone):
    def __init__(self,name,rect,screen):
        DropZone.__init__(self, name, rect)
        self.image.fill((128,0,0))
        self.screen = screen
        self.coordinates = rect.center
        
        self.Xpos = self.coordinates[0]
        self.Ypos = self.coordinates[1]
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))

class TestZone(DropZone):
    def __init__(self,name,rect,screen):
        DropZone.__init__(self, name, rect)
        self.screen = screen
        
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))

class MixingScreen(Screen):
    def __init__(self, game, materials, newMaterials):
        self.dropBig = MixZone('bigDrop', pygame.Rect(200, 300, 200, 200), self, game)
        self.dropMats = HoldZone('holdsMaterials', pygame.Rect(487.5, 0, 50, WINDOWHEIGHT), game)
        self.dropNewMats = HoldZone('holdsNewMaterials', pygame.Rect(0,0, 50, WINDOWHEIGHT), game)
        self.game = game
        self.materials = materials
        self.newMaterials = newMaterials
        self.materialNotificationLabel = None
        self.Notificationlabels = []
        
        self.forceScreenButton = MatSciGame.ForceScreenButton("forceScreen","setbut.png",pygame.Rect(600,0,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),MatSciGame.ForceScreenButton.clicked, self.game)
                        
        
        self.materials.append(MatSciGame.Material("glass", 50, 100, pygame.Rect((500, 0, 20, 20))))
        self.materials.append(MatSciGame.Material("aluminuim", 30, 70, pygame.Rect((500, 1* WINDOWHEIGHT/5, 20, 20))))
        self.materials.append(MatSciGame.Material("plastic", 65, 10, pygame.Rect((500, 2* WINDOWHEIGHT/5, 20, 20))))
        self.materials.append(MatSciGame.Material("gold", 30, 60, pygame.Rect((500, 3* WINDOWHEIGHT/5, 20, 20))))
        self.materials.append(MatSciGame.Material("copper", 40, 50, pygame.Rect((500, 4* WINDOWHEIGHT/5, 20, 20))))
                        
        self.dropZones = [self.dropBig, self.dropMats, self.dropNewMats]
        
        self.actors = self.dropZones + self.materials + self.newMaterials
        
        if isinstance(self.materialNotificationLabel, planes.Plane):        
            self.actors.append(self.materialNotificationLabel)
        
        self.buttons = [self.forceScreenButton]

        Screen.__init__(self, self.buttons, self.actors, (0,128,0))
    
    def update(self):
        if len(self.Notificationlabels) > 0:
            time = pygame.time.get_ticks()
            if (self.dropBig.creationTime > 0) and (time - self.dropBig.creationTime < 1000):
                pass
            else:
                self.dropBig.creationTime = 0
                self.materialNotificationLabel = None
                self.labels = []
                self.actors = self.dropZones + self.materials + self.newMaterials

class ForceTestScreen(Screen):
    def __init__(self, game, materials, newMaterials):
        dropTest = TestZone('dropTest', pygame.Rect(0,0, 200, 200), self)
        self.game = game
        self.materials = materials
        self.newMaterials = newMaterials
        self.dropZones = [dropTest]
        self.mixScreenButton = MatSciGame.MixScreenButton("mixScreen","tutbut.png",pygame.Rect(600,0,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),MatSciGame.ForceScreenButton.clicked, self.game)
                 
        self.actors = self.dropZones+self.materials+self.newMaterials
        self.buttons = [self.mixScreenButton]
        
        Screen.__init__(self, self.buttons, self.actors, (128,0,0))


