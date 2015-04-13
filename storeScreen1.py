# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 18:49:26 2014

@author: anneubuntu
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 00:32:11 2014

@author: anneubuntu
"""
import pygame
import planes
from collections import deque
from screen import Screen
from screen import Button
from screen import DropZone
import time
from screen import ScreenText

MOVEBUTTON_HEIGHT = 75
MOVEBUTTON_WIDTH = 50

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750


scrleft = 50
scrright = 1150
scrtop = 50
scrbottom = 700


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Upgrade(planes.Plane):
    def __init__(self, name, rect, im, cost, value, order, model, draggable=True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.position = rect.center
        self.Xpos = self.position[0]
        self.Ypos = self.position[1]
        self.cost = cost
        self.im = im
        self.image = pygame.image.load(im)
        self.value = value
        self.width = rect.width
        self.height = rect.height
        self.order = order
        self.model = model
        self.origRect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)
        font1 = pygame.font.SysFont("Arial", 20)
        self.description = ScreenText("desc", "Cost: "+str(self.cost), pygame.Rect(self.Xpos+self.width/2, self.Ypos+self.height/2, 100, 20), font1)

    def mouseover_callback(self):
        if isinstance(self.model, StoreScreen):
            self.model.actors.append(self.description)

    def mouseout_callback(self):
        if isinstance(self.model, StoreScreen):
            names = [actor.name for actor in self.model.actors]
            if self.description.name in names:
                index = names.index(self.description.name)
                del(self.model.actors[index])
            self.model.actors = self.model.actorsWithoutDesc

class MotorUpgrade(Upgrade):
    def __init__(self, name, rect, im, cost, value, order, model):
        Upgrade.__init__(self, name, rect, im, cost, value, order, model)

class BumperUpgrade(Upgrade):
    def __init__(self, name, rect, im, cost, value, order, model):
        Upgrade.__init__(self, name, rect, im, cost, value, order, model)

class BuildButton(Button):
    def __init__(self, label, rect, im, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.buildscreen

class BuyButton(Button):
    def __init__(self, label, rect, im, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load(im)
    def clicked(self, button_name):
        self.model.moneyLabel.updateBackground((0,255,0,100))
        if self.model.robot.money >= self.model.shoppingcart.costincart:
            lis = self.model.shoppingcart.thingsDroppedOnMe
            for i in range(len(lis)):
                upgrade = lis[i]
                self.model.robot.money -= upgrade.cost
                if isinstance(upgrade, MotorUpgrade):
                    self.model.game.purchases.append(MotorUpgrade("b"+str(pygame.time.get_ticks()), upgrade.origRect, upgrade.im, upgrade.cost, upgrade.value, upgrade.order, None))
                if isinstance(upgrade, BumperUpgrade):
                    self.model.game.purchases.append(BumperUpgrade("b"+str(pygame.time.get_ticks()), upgrade.origRect, upgrade.im, upgrade.cost, upgrade.value, upgrade.order, None))
                time.sleep(.01)
            for upgrade in lis:
                names = [actor.name for actor in self.model.actors]
                if upgrade.name in names:
                    index = names.index(upgrade.name)
                    del(self.model.actors[index])
            self.model.shoppingcart.thingsDroppedOnMe = []


class ShoppingCart(DropZone):
    def __init__(self, name, rect, model):
        DropZone.__init__(self, name, rect)
        self.model = model
        self.costincart = 0

    def dropped_upon(self, plane, coordinates):
        planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))
        plane.moving = False
        self.thingsDroppedOnMe.append(plane)

    def checkDroppedUpon(self):
        newThingsInMe = []
        for thing in self.thingsDroppedOnMe:
            if self.rect.colliderect(thing.rect):
                newThingsInMe.append(thing)
        self.thingsDroppedOnMe = newThingsInMe

    def calculateCostInCart(self):
        newCost = 0
        for thing in self.thingsDroppedOnMe:
            newCost += thing.cost
        self.costincart = newCost


class StoreScreen(Screen):
    def __init__(self, robot, game):
        self.robot = robot
        self.game = game
        self.startPosition = (400,400)
        start = BuildButton("tobuildscreen", pygame.Rect(scrright-200, scrbottom-100, 200, 100), "img/back_button_big.png", BuildButton.clicked, self)
        buy = BuyButton("buythings", pygame.Rect(500, scrbottom-140, 400,150), "img/buy_button.png", BuyButton.clicked, self)
        font1 = pygame.font.SysFont("Arial", 40)
        self.moneyLabel = ScreenText("moneytext", "Money: "+str(self.robot.money), pygame.Rect(WINDOWWIDTH-225, 0, 200, 50), font1)
        motorLabel = planes.Plane("motorLabel", pygame.Rect(scrleft,scrtop,170,50), draggable=False, grab=False)
        motorLabel.image = pygame.image.load("img/motorupgrade_label.png")
        mu1 = MotorUpgrade("mu1", pygame.Rect(scrleft,scrtop+60,50,50), "img/motorupgrade_1.png", 100, 0.3, 1, self)
        mu2 = MotorUpgrade("mu2", pygame.Rect(scrleft+60,scrtop+60,50,50), "img/motorupgrade_2.png", 200, 0.2, 2, self)
        mu3 = MotorUpgrade("mu3", pygame.Rect(scrleft+120,scrtop+60,50,50), "img/motorupgrade_3.png", 300, 0.1, 3, self)
        self.shoppingcart = ShoppingCart("shoppingcart", pygame.Rect(350,50,800,600), self)
        self.shoppingcart.image = pygame.image.load("img/shoppingcart.png")

        bumperLabel = planes.Plane("bumperLabel", pygame.Rect(scrleft, mu3.rect.bottom + 30, 170, 50), draggable=False, grab=False)
        bumperLabel.image = pygame.image.load("img/bumperupgrade_label.png")
        bu1 = BumperUpgrade("bu1", pygame.Rect(scrleft, bumperLabel.rect.bottom + 10, 50, 50), "img/bumperupgrade_1.png", 100, 7, 1, self)
        bu2 = BumperUpgrade("bu2", pygame.Rect(scrleft+60, bumperLabel.rect.bottom + 10, 50, 50), "img/bumperupgrade_2.png", 200, 5, 2, self)
        bu3 = BumperUpgrade("bu3", pygame.Rect(scrleft+120, bumperLabel.rect.bottom + 10, 50, 50), "img/bumperupgrade_3.png", 300, 3, 3, self)
        self.costInCartlabel = ScreenText("costincart", "Cost in Cart: 0", pygame.Rect(500, 50, 400, 50), font1)

        buttons = [start, buy]
        self.upgrades = [mu1, mu2, mu3, bu1, bu2, bu3]
        self.actorsWithoutDesc = [self.shoppingcart, motorLabel, bumperLabel, self.moneyLabel, self.costInCartlabel] + self.upgrades
        self.actors = self.actorsWithoutDesc
        Screen.__init__(self,buttons,self.actors,BLACK)

    def update(self):
        self.moneyLabel.updateText("Money: "+str(self.robot.money))
        self.shoppingcart.checkDroppedUpon()
        self.shoppingcart.calculateCostInCart()
        self.costInCartlabel.updateText("Cost in Cart: "+str(self.shoppingcart.costincart))
        if self.shoppingcart.costincart > self.robot.money:
            self.costInCartlabel.updateColor((255,0,0))
        else:
            self.costInCartlabel.updateColor(WHITE)