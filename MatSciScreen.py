
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
from screen import DropZone
import MatSciGame


class MixZone(DropZone):
    def __init__(self,name,rect,screen):
        DropZone.__init__(self,name, rect)
        self.screen = screen
        
        self.firstDropped = None
        self.firstDroppedCoordinates = None
        
        self.secondDropped = None
        self.secondDroppedCoordinates = None
        self.thingsDropped = 0
        
        
    def dropped_upon(self, plane, coordinates):
       self.thingsDropped +=1
       planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))
       
       if self.thingsDropped == 1:
           self.firstDropped = plane
           self.firstDroppedCoordinates = coordinates
           
           if isinstance(self.get_plane_at(self.firstDroppedCoordinates), MatSciGame.Material):
               self.thingsDropped -=1
               print self.thingsDropped
       
       if self.thingsDropped == 2:
           self.secondDropped = plane
           self.secondDroppedCoordinates = coordinates
           
           self.screen.newMaterials.append((MatSciGame.Material("Newmat"+`len(self.screen.newMaterials)`, pygame.Rect((100, (len(self.screen.newMaterials)+1)*60, 20, 20)))))
           self.screen.actors =  self.screen.dropZones + self.screen.materials + self.screen.newMaterials
           self.thingsDropped = 0

class MixingScreen(Screen):
    def __init__(self, game):
        dropBig = MixZone('bigDrop', pygame.Rect(200, 300, 200, 200), self)
        self.game = game
        self.materials = []
        self.newMaterials = []
        for i in range(0,4):
            self.materials.append(MatSciGame.Material("mat"+str(i), pygame.Rect((500, i* 600/(len(self.materials)+1), 20, 20))))
        self.dropZones = [dropBig]
        self.actors = self.dropZones + self.materials + self.newMaterials

        Screen.__init__(self, [], self.actors, (0,128,0))

