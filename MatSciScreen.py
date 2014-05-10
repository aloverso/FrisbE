
import sys

# Add current and parent directory. One of them is supposed to contain the
# planes package.
#
sys.path.append("../")
sys.path.append("./")

import pygame
import planes
from planes import *
from collections import deque
from screen import Screen
from screen import Button
from screen import DropZone
from screen import ScreenText
import MatSciGame

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class MixZone(DropZone):
    def __init__(self,name,rect,screen, model):
        DropZone.__init__(self, name, rect)
        self.image = pygame.image.load("Blender2.png")
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
           if self.screen.game.money - 1000 < 0:
               self.screen.Notificationlabels.append(ScreenText("textBad", "Too Little Money!!" , pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 250, 50), pygame.font.SysFont("Arial", 40)))
               
               planes.Plane.dropped_upon(self.screen.dropMats, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))

               planes.Plane.dropped_upon(self.screen.dropMats, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))

               
               
               self.creationTime = pygame.time.get_ticks()
               self.thingsDropped = 0
               self.screen.actors =  self.screen.dropZones + self.screen.materials + self.screen.newMaterials + self.screen.constantLabels + self.screen.Notificationlabels
           
           else:  
               self.screen.game.money = self.screen.game.money - 1000
    
               
               self.secondDropped = plane
               self.secondDroppedCoordinates = coordinates
               
               self.screen.Notificationlabels.append(ScreenText("text1", "Made a New Material", pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 200, 50), pygame.font.SysFont("Arial", 40)))
               newStrength = int(2*(self.firstDropped.strength + self.secondDropped.strength)/3)
               newMeltingPoint = int(2*(self.firstDropped.meltingPoint + self.secondDropped.meltingPoint)/3)
               newAppearence = int(2*(self.firstDropped.appearence + self.secondDropped.appearence)/3)
               
               newTier = self.firstDropped.tier + self.secondDropped.tier
               
               if len(self.screen.newMaterials) < 9:
                   self.screen.newMaterials.append((MatSciGame.Material("Newmat"+`len(self.screen.newMaterials)`, newStrength, False, newMeltingPoint, False, newAppearence, newTier, pygame.Rect((150/2 + 20, 150+50*len(self.screen.newMaterials), 50, 50)), self.screen.game)))
               elif len(self.screen.newMaterials) < 18:
                   self.screen.newMaterials.append((MatSciGame.Material("Newmat"+`len(self.screen.newMaterials)`, newStrength, False, newMeltingPoint, False, newAppearence, newTier, pygame.Rect((150/2 + 110, 150+50*(len(self.screen.newMaterials)-9), 50, 50)), self.screen.game)))           
               else:
                    self.screen.Notificationlabels.append(ScreenText("text3", "Too Many Materials!!", pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2), pygame.font.SysFont("Arial", 40)))
               planes.Plane.dropped_upon(self.screen.dropMats, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
               planes.Plane.dropped_upon(self.screen.dropMats, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
               self.screen.actors =  self.screen.dropZones + self.screen.materials + self.screen.newMaterials + self.screen.constantLabels + self.screen.Notificationlabels
               self.thingsDropped = 0
               self.creationTime = pygame.time.get_ticks()
                             
    def getFirstTick(self):
        self.firstTick = self.model.clock.tick()
        return self.firstTick               
                      
class ItemMakeZone(DropZone):
    def __init__(self,name,rect,screen, model):
        DropZone.__init__(self, name, rect)
        self.screen = screen
        self.model = model
        self.image = pygame.image.load("AnvilAndHammer.png")
        
        self.firstDropped = None
        self.firstDroppedCoordinates = None
        
        self.secondDropped = None
        self.secondDroppedCoordinates = None
        self.thingsDropped = 0
        self.creationTime = 0
        
    def dropped_upon(self, plane, coordinates):
       name = 0
       self.thingsDropped +=1

       planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))
       
       if self.thingsDropped == 1:
           
           self.firstDropped = plane
           self.firstDroppedCoordinates = coordinates
                
       if self.thingsDropped == 2:

           self.secondDropped = plane
           self.secondDroppedCoordinates = coordinates
                     
           if isinstance(self.firstDropped, MatSciGame.Material) and isinstance(self.secondDropped, MatSciGame.Material):
               
               self.screen.Notificationlabels.append(ScreenText("textBad", "You need an item and a material" , pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 250, 50), pygame.font.SysFont("Arial", 40)))
               
                              
               if isinstance(self.firstDropped, MatSciGame.Material):
                   planes.Plane.dropped_upon(self.screen.dropMats, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
               else:
                   planes.Plane.dropped_upon(self.screen.dropItems, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
           
               if isinstance(self.secondDropped, MatSciGame.Material):
                   planes.Plane.dropped_upon(self.screen.dropMats, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
               else:
                   planes.Plane.dropped_upon(self.screen.dropItems, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
               
               
               self.creationTime = pygame.time.get_ticks()
               self.thingsDropped = 0
               self.screen.actors =  self.screen.dropZones + self.screen.materials + self.screen.newMaterials + self.screen.constantLabels + self.screen.items + self.screen.Notificationlabels
                                             
           elif isinstance(self.firstDropped, MatSciGame.Item) and isinstance(self.secondDropped, MatSciGame.Item):
               
               self.screen.Notificationlabels.append(ScreenText("textBad", "You need an item and a material" , pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 200, 50), pygame.font.SysFont("Arial", 40)))
                                                     
               if isinstance(self.firstDropped, MatSciGame.Material):
                   planes.Plane.dropped_upon(self.screen.dropMats, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
                   
               else:
                   planes.Plane.dropped_upon(self.screen.dropItems, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
           
               if isinstance(self.secondDropped, MatSciGame.Material):
                   planes.Plane.dropped_upon(self.screen.dropMats, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
               else:
                   planes.Plane.dropped_upon(self.screen.dropItems, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
               
               self.creationTime = pygame.time.get_ticks()
               self.thingsDropped = 0
               self.screen.actors =  self.screen.dropZones + self.screen.materials + self.screen.newMaterials + self.screen.constantLabels + self.screen.items + self.screen.Notificationlabels
           
           else:
               if isinstance(self.firstDropped, MatSciGame.Material):
                   theMaterial = self.firstDropped
                   theItem = self.secondDropped
               
               else:
                   theMaterial = self.secondDropped
                   theItem = self.firstDropped
                   
               if theMaterial.strengthTested == False or theMaterial.meltingPointTested == False:
                   self.screen.Notificationlabels.append(ScreenText("textBad2", "You need to test this material" , pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 200, 50), pygame.font.SysFont("Arial", 40)))
                                                     
                   if isinstance(self.firstDropped, MatSciGame.Material):
                       planes.Plane.dropped_upon(self.screen.dropMats, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
                       
                   else:
                       planes.Plane.dropped_upon(self.screen.dropItems, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
               
                   if isinstance(self.secondDropped, MatSciGame.Material):
                       planes.Plane.dropped_upon(self.screen.dropMats, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
                   else:
                       planes.Plane.dropped_upon(self.screen.dropItems, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
                   
                   self.creationTime = pygame.time.get_ticks()
                   self.thingsDropped = 0
                   self.screen.actors =  self.screen.dropZones + self.screen.materials + self.screen.newMaterials + self.screen.constantLabels + self.screen.items + self.screen.Notificationlabels
                   
               else:
#                  Wow you have actually made an item this time! Way to go!
                   
                   meltMoney = 1000 - (abs(theItem.bestMeltingPoint - theMaterial.meltingPoint))*1000*theItem.meltImport/theItem.bestMeltingPoint
                   strengthMoney = 1000 - (abs(theItem.bestStrength - theMaterial.strength))*1000*theItem.strengthImport/theItem.bestStrength
                   appearenceMoney = 1000 - (abs(theItem.appearenceNeed - theMaterial.appearence))*1000*theItem.appearImport/theItem.appearenceNeed
                   
                   totalMoney = int(meltMoney*theItem.meltImport + strengthMoney*theItem.strengthImport + appearenceMoney*theItem.appearImport)
                   
                   self.screen.game.money = self.screen.game.money + totalMoney
                   
                   newItem = (MatSciGame.CreatedItem(theItem.name, BLUE, theMaterial.strength, theMaterial.meltingPoint, theMaterial.appearence, theMaterial, totalMoney, self.screen.game))
                   name += 1
                   
                   if theItem.name == "cup":
                       if len(self.screen.game.topCups) < 3:
                           self.screen.game.topCups.append(newItem)

                       else:
                           minimum = 700000000
                           for item in self.screen.game.topCups:
                               if item.money < minimum:
                                   minimum = item.money
                                   smallItem = item
                           
                           if newItem.money > min:
                               self.screen.game.topCups[self.screen.game.topCups.index(smallItem)] = newItem
                   
                   if theItem.name == "hammer":
                       if len(self.screen.game.topHammers) < 3:
                           self.screen.game.topHammers.append(newItem)

                       else:
                           for item in self.screen.game.topHammers:
                               if newItem.money > item.money:
                                   self.screen.game.topHammers.remove(item)
                                   self.screen.game.topHammers.append(newItem)
                   if theItem.name == "poker":
                       if len(self.screen.game.topPokers) < 3:
                           self.screen.game.topPokers.append(newItem)

                       else:
                           for item in self.screen.game.topPokers:
                               if newItem.money > item.money:
                                   self.screen.game.topPokers.remove(item)
                                   self.screen.game.topPokers.append(newItem)
#                   if theItem.name == "cup":
#                       if len(self.screen.game.topCups) < 3:
#                           self.screen.game.topCups.append(newItem)
#                           print "appended the new item!"
#                       else:
#                           for item in self.screen.game.topCups:
#                               if newItem.money > item.money:
#                                   self.screen.game.topCups.remove(item)
#                                   self.screen.game.topCups.append(newItem)
#                   if theItem.name == "cup":
#                       if len(self.screen.game.topCups) < 3:
#                           self.screen.game.topCups.append(newItem)
#                           print "appended the new item!"
#                       else:
#                           for item in self.screen.game.topCups:
#                               if newItem.money > item.money:
#                                   self.screen.game.topCups.remove(item)
#                                   self.screen.game.topCups.append(newItem)
                   
                   self.screen.Notificationlabels.append(ScreenText("text1", "Made a New Item!", pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 250, 50), pygame.font.SysFont("Arial", 40)))
    
                   #Dependent on whether you're putting back a material or item
#                   self.screen.actors.remove(theMaterial)
#                   self.screen.game.newMaterials.remove(theMaterial)
                             
                   if isinstance(self.secondDropped, MatSciGame.Item):
                       planes.Plane.dropped_upon(self.screen.dropItems, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
                       planes.Plane.dropped_upon(self.screen.dropMats, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
                   else:
                       planes.Plane.dropped_upon(self.screen.dropItems, self.firstDropped, (self.firstDropped.Xpos, self.firstDropped.Ypos))
                       planes.Plane.dropped_upon(self.screen.dropMats, self.secondDropped, (self.secondDropped.Xpos, self.secondDropped.Ypos))
                       
                  
                   self.thingsDropped = 0               
                   self.creationTime = pygame.time.get_ticks()
                   self.screen.actors =  self.screen.dropZones + self.screen.materials + self.screen.newMaterials + self.screen.constantLabels + self.screen.items + self.screen.Notificationlabels
    

            
class HoldZone(DropZone):
    def __init__(self,name,rect,screen):
        DropZone.__init__(self, name, rect)
        if self.name == "holdMats":
            self.image = pygame.image.load("HoldMats.png")
        else:
            self.image = pygame.image.load("HoldNewMats.png")
        self.screen = screen
        self.coordinates = rect.center
        
        self.Xpos = self.coordinates[0]
        self.Ypos = self.coordinates[1]
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))

class StrengthTestZone(DropZone):
    def __init__(self,name,rect,screen):
        DropZone.__init__(self, name, rect)
        self.screen = screen
        self.image = pygame.image.load("ForceTester.png")
        
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self.screen.dropMats, plane, (plane.Xpos, plane.Ypos))
       
       self.screen.Notificationlabels.append(ScreenText("text1", "Strength is " + str(plane.strength), pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 200, 50), pygame.font.SysFont("Arial", 40)))
       plane.strengthTested = True
       self.screen.actors =  self.screen.actors + self.screen.Notificationlabels
       self.creationTime = pygame.time.get_ticks()

class MeltingTestZone(DropZone):
    def __init__(self,name,rect,screen):
        DropZone.__init__(self, name, rect)
        self.image = pygame.image.load("Oven.PNG")
        self.screen = screen
        
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self.screen.dropMats, plane, (plane.Xpos, plane.Ypos))
       
       self.screen.Notificationlabels.append(ScreenText("text1", "Melting Point is " + str(plane.meltingPoint), pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 200, 50), pygame.font.SysFont("Arial", 40)))
       plane.meltingPointTested = True
       self.screen.actors =  self.screen.actors + self.screen.Notificationlabels
       self.creationTime = pygame.time.get_ticks()

class MixingScreen(Screen):
    def __init__(self, game, materials, newMaterials, money):
        self.dropBig = MixZone('bigDrop', pygame.Rect(300+(150/2), 200, 300, 300), self, game)
        self.dropMats = HoldZone('holdMats', pygame.Rect(730, 100, 90, 550), game)
        self.dropNewMats = HoldZone('holdsNewMaterials', pygame.Rect(150/2,100, 180, 550), game)
        
        self.money = money
        self.game = game
        self.materials = materials
        self.newMaterials = newMaterials

        self.Notificationlabels = []
        self.constantLabels = []
        self.infoLabels = []
        self.infoCreationTime = 0
        
        self.forceScreenButton = MatSciGame.ForceScreenButton("forceScreen", "StrengthButton.png",pygame.Rect(900, 150, 300, 75),MatSciGame.ForceScreenButton.clicked, self.game)
        self.heatScreenButton = MatSciGame.HeatScreenButton("heatScreen", "FireButton2.png", pygame.Rect(900, 300, 300, 75),MatSciGame.HeatScreenButton.clicked, self.game)
        self.itemScreenButton = MatSciGame.ItemScreenButton("itemScreen", "MakeNewItemsButton.png", pygame.Rect(900, 450, 300, 75),MatSciGame.ItemScreenButton.clicked, self.game)
        self.itemViewScreenButton = MatSciGame.ItemViewScreenButton("itemviewScreen", "ViewItemsButton.png", pygame.Rect(900, 600, 300, 75),MatSciGame.ItemScreenButton.clicked, self.game)
        
        self.constantLabels.append(ScreenText("moneyText", "Money = " + str(self.money), pygame.Rect(900, 0, 300, 75), pygame.font.SysFont("Arial", 40)))               
        
        self.materials.append(MatSciGame.Material("glass", 50, True, 100, True, 100, 1, pygame.Rect((750, 150, 50, 50)), self.game))
        self.materials.append(MatSciGame.Material("aluminuim", 30, True, 70, True, 70, 1, pygame.Rect((750, 250, 50, 50)), self.game))
        self.materials.append(MatSciGame.Material("plastic", 65, True, 10, True, 50, 1, pygame.Rect((750, 350, 50, 50)), self.game))
        self.materials.append(MatSciGame.Material("gold", 30, True, 60, True, 100, 1,pygame.Rect((750, 450, 50, 50)), self.game))
        self.materials.append(MatSciGame.Material("copper", 40, True, 50, True, 40, 1, pygame.Rect((750, 550, 50, 50)), self.game))
                        
        self.dropZones = [self.dropBig, self.dropMats, self.dropNewMats]
        self.buttonArray = [self.forceScreenButton, self.heatScreenButton, self.itemScreenButton, self.itemViewScreenButton]
        
        self.actors = self.dropZones + self.constantLabels + self.materials + self.buttonArray + self.newMaterials
        
        if len (self.Notificationlabels) > 0:        
            self.actors = self.actors + self.Notificationlabels
        
        

        Screen.__init__(self, [], self.actors, "labBackground.png")
    
    def update(self):
        self.constantLabels[0].updateText("Money = " + str(self.game.money))
        if len(self.Notificationlabels) > 0:
            time = pygame.time.get_ticks()
            if (self.dropBig.creationTime > 0) and (time - self.dropBig.creationTime < 2000):
                pass
            else:

                self.dropBig.creationTime = 0
                self.labels = []
                self.actors = self.dropZones+self.materials + self.buttonArray + self.newMaterials + self.constantLabels + self.infoLabels
        else:
            self.actors = self.dropZones + self.materials + self.buttonArray + self.newMaterials + self.constantLabels + self.infoLabels      
        
class ForceTestScreen(Screen):
    def __init__(self, game, materials, newMaterials, money):
        
        self.dropTest = StrengthTestZone('dropTest', pygame.Rect(300, 200, 300, 300), self)
        self.dropMats = HoldZone('holdMats', pygame.Rect(730, 100, 90, 550), game)
        self.dropNewMats = HoldZone('holdsNewMaterials', pygame.Rect(150/2,100, 180, 550), game)
        self.money = money
        
        self.game = game
  
        self.materials = materials
        self.newMaterials = newMaterials
        self.constantLabels = []
        self.dropZones = [self.dropTest, self.dropMats, self.dropNewMats]
        self.mixScreenButton = MatSciGame.MixScreenButton("mixScreen","MixingButton.png", pygame.Rect(900, 300, 300, 75),MatSciGame.ForceScreenButton.clicked, self.game)
        
        
        self.constantLabels.append(ScreenText("moneyText", "Money = " + str(self.money), pygame.Rect(900, 0, 300, 75), pygame.font.SysFont("Arial", 40)))               
        
        self.Notificationlabels = []
        self.infoLabels = []
        
        self.actors = self.constantLabels + self.dropZones+ self.materials+self.newMaterials
        self.buttons = [self.mixScreenButton]
        
        Screen.__init__(self, self.buttons, self.actors, "woodBackground.png")
    
    def update(self):
        self.constantLabels[0].updateText("Money = " + str(self.game.money))
        if len(self.Notificationlabels) > 0:
            time = pygame.time.get_ticks()
            if (self.dropTest.creationTime > 0) and (time - self.dropTest.creationTime < 2000):
                pass
            else:
                self.dropTest.creationTime = 0
                self.materialNotificationLabel = None
                self.labels = []
                self.actors = self.dropZones + self.materials + self.newMaterials + self.constantLabels + self.infoLabels
        else:
            self.actors = self.dropZones + self.materials + self.newMaterials + self.constantLabels + self.infoLabels

class MeltingTestScreen(Screen):
    def __init__(self, game, materials, newMaterials, money):
        
        self.dropTest = MeltingTestZone('dropTest', pygame.Rect(290, 200, 300, 300), self)
        self.dropMats = HoldZone('holdMats', pygame.Rect(730, 100, 90, 550), game)
        self.dropNewMats = HoldZone('holdsNewMaterials', pygame.Rect(150/2,100, 180, 550), game)
        self.money = money
        
        self.game = game

        
        self.materials = materials
        self.newMaterials = newMaterials

        
        
        self.constantLabels = []
        self.dropZones = [self.dropTest, self.dropMats, self.dropNewMats]
        self.mixScreenButton = MatSciGame.MixScreenButton("mixScreen","MixingButton.png", pygame.Rect(900, 300, 300, 75),MatSciGame.ForceScreenButton.clicked, self.game)
        
        self.constantLabels.append(ScreenText("moneyText", "Money = " + str(self.money), pygame.Rect(900, 0, 300, 75), pygame.font.SysFont("Arial", 40)))               
        
        
        
        self.Notificationlabels = []
        self.infoLabels = []
        
        self.actors = self.constantLabels + self.dropZones+ self.materials+self.newMaterials
        self.buttons = [self.mixScreenButton]
        
        Screen.__init__(self, self.buttons, self.actors, "kitchenBackground.png")
    
    def update(self):
        self.constantLabels[0].updateText("Money = " + str(self.game.money))
        if len(self.Notificationlabels) > 0:
            time = pygame.time.get_ticks()
            if (self.dropTest.creationTime > 0) and (time - self.dropTest.creationTime < 2000):
                pass
            else:
                self.dropTest.creationTime = 0
                self.materialNotificationLabel = None
                self.labels = []
                self.actors = self.dropZones + self.materials + self.newMaterials + self.constantLabels + self.infoLabels
        else:
            self.actors = self.dropZones + self.materials + self.newMaterials + self.constantLabels + self.infoLabels
            

class ItemMakeScreen(Screen):
    def __init__(self, game, materials, newMaterials, money):
        
        self.dropTest = ItemMakeZone('makeItems', pygame.Rect(300, 200, 450, 450), self, game)
        self.dropMats = HoldZone('holdMats', pygame.Rect(730, 100, 90, 550), game)
        self.dropNewMats = HoldZone('holdsNewMaterials', pygame.Rect(150/2,100, 180, 550), game)
        self.dropItems = HoldZone('holdsItems', pygame.Rect(650,625, 300, WINDOWHEIGHT/2), game)
        self.money = money
        
        self.game = game

        
        self.materials = materials
        self.newMaterials = newMaterials
        self.items = []
        
        self.items.append(MatSciGame.Item("cup", pygame.Rect(300, 600, 85, 93), 60, 50, 70, .3, .1, .6, (0,0,0)))
        self.items.append(MatSciGame.Item("hammer", pygame.Rect(400, 600, 90, 90), 100, 60, 40, .6, .3, .1, (0,0,0)))
        self.items.append(MatSciGame.Item("table", pygame.Rect(650, 600, 85, 70), 80, 40, 60, .5, .2, .3, (0,0,0)))
        self.items.append(MatSciGame.Item("poker", pygame.Rect(500, 600, 34, 90), 40, 100, 30, .2, .7, .1, (0,0,0)))
        self.items.append(MatSciGame.Item("decor", pygame.Rect(550, 600, 80, 90), 20, 40, 100, .2, .1, .7, (0,0,0)))
        
        self.constantLabels = []
        self.dropZones = [self.dropTest, self.dropMats, self.dropNewMats]
        self.mixScreenButton = MatSciGame.MixScreenButton("mixScreen","MixingButton.png", pygame.Rect(900, 300, 300, 75),MatSciGame.ForceScreenButton.clicked, self.game)
        
        self.constantLabels.append(ScreenText("moneyText", "Money = " + str(self.money), pygame.Rect(900, 0, 300, 75), pygame.font.SysFont("Arial", 40)))               
        
        self.Notificationlabels = []
        self.infoLabels = []
        
        self.actors = self.constantLabels + self.dropZones+ self.materials+self.newMaterials + self.items
        self.buttons = [self.mixScreenButton]
        
        Screen.__init__(self, self.buttons, self.actors, "smithBackground.png")
    
    def update(self):
        self.constantLabels[0].updateText("Money = " + str(self.game.money))
        if len(self.Notificationlabels) > 0:
            time = pygame.time.get_ticks()
            if (self.dropTest.creationTime > 0) and (time - self.dropTest.creationTime < 2000):
                pass
            else:
                self.dropTest.creationTime = 0
                self.materialNotificationLabel = None
                self.labels = []
                self.actors = self.dropZones + self.materials + self.newMaterials + self.constantLabels + self.infoLabels + self.items
        else:
            self.actors = self.dropZones + self.materials + self.newMaterials + self.constantLabels + self.infoLabels + self.items

class ItemViewScreen(Screen):
    def __init__(self, game, materials, newMaterials, money):
        
        self.money = money
        
        self.game = game

        
        self.materials = materials
        self.newMaterials = newMaterials
        
        self.constantLabels = []
        self.shownItems = []

        self.mixScreenButton = MatSciGame.MixScreenButton("mixScreen","MixingButton.png", pygame.Rect(900, 300, 300, 75),MatSciGame.ForceScreenButton.clicked, self.game)
        
        self.constantLabels.append(ScreenText("moneyText", "Money = " + str(self.money), pygame.Rect(900, 0, 300, 75), pygame.font.SysFont("Arial", 40)))               
        
        self.Notificationlabels = []
        self.infoLabels = []
        
        self.actors = self.constantLabels + self.shownItems
        
        self.buttons = [self.mixScreenButton]
        
        Screen.__init__(self, self.buttons, self.actors, "bookOpen.png")
    
    def update(self):
#        self.shownItems = []
        self.constantLabels[0].updateText("Money = " + str(self.game.money))
        if len(self.game.topCups) > 0:
            for i in range (len(self.game.topCups)):
                cup = self.game.topCups[i]
                cup.setName("topCup" + `i`)
                cup.setRect(pygame.Rect(50, i*150+WINDOWWIDTH/5, 100, 100))
                self.shownItems.append(cup)
            self.actors =  self.shownItems + self.constantLabels + self.infoLabels
        
        if len(self.game.topHammers) > 0:
            for i in range (len(self.game.topHammers)):
                hammer = self.game.topHammers[i]
                hammer.setName("topHammer" + `i`)
                hammer.setRect(pygame.Rect(160, i*150+WINDOWWIDTH/5, 100, 100))
                self.shownItems.append(hammer)
            self.actors =  self.shownItems + self.constantLabels + self.infoLabels
        
        if len(self.game.topTables) > 0:
            for i in range (len(self.game.topTables)):
                table = self.game.topTables[i]
                table.setName("topTable" + `i`)
                table.setRect(pygame.Rect(220, i*150+WINDOWWIDTH/5, 100, 100))
                self.shownItems.append(table)
            self.actors =  self.shownItems + self.constantLabels + self.infoLabels
        
        if len(self.game.topPokers) > 0:
            for i in range (len(self.game.topPokers)):
                poker = self.game.topPokers[i]
                poker.setName("topPoker" + `i`)
                poker.setRect(pygame.Rect(350, i*150+WINDOWWIDTH/5, 100, 100))
                self.shownItems.append(poker)
            self.actors =  self.shownItems + self.constantLabels + self.infoLabels
        
        if len(self.game.topDecors) > 0:
            for i in range (len(self.game.topDecors)):
                decor = self.game.topCups[i]
                decor.setName("topDecor" + `i`)
                decor.setRect(pygame.Rect(460, i*150+WINDOWWIDTH/5, 100, 100))
                self.shownItems.append(decor)
            self.actors =  self.shownItems + self.constantLabels + self.infoLabels
        else:
            self.actors = self.constantLabels + self.shownItems + self.infoLabels