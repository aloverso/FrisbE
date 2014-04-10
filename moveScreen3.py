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

MOVEBUTTON_HEIGHT = 75
MOVEBUTTON_WIDTH = 50

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Robot(planes.Plane):
    def __init__(self, x, y, width, height, name, im):
	planes.Plane.__init__(self, name, pygame.Rect(x,y,width,height), draggable=False, grab=False)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vx = 0.0
        self.vy = 0.0
        #self.image = pygame.image.load(im)
        self.image.fill(im)
    
    def update(self):
        '''updates the actor's position and updates the rectangle object of the
        actor'''
        self.x += self.vx
        self.y += self.vy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class UpButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("up.png")
    def clicked(self, button_name):
        self.model.addCommand("up.png", 0, 1)

class DownButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("down.png")
    def clicked(self, button_name):
        self.model.addCommand("down.png", 0, -1)

class LeftButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("left.png")
    def clicked(self, button_name):
        self.model.addCommand("left.png", -1, 0)

class RightButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("right.png")
    def clicked(self, button_name):
        self.model.addCommand("right.png", 1, 0)

class Command(planes.Plane):
    def __init__(self, robot, im, xMove, yMove, rect, name):
        planes.Plane.__init__(self, name, rect, draggable=False, grab=False)
        self.image = pygame.image.load(im)
        self.xMove = xMove
        self.yMove = yMove
        self.robot = robot
    def update(self):
        pass
   
class MoveScreen(Screen):
    def __init__(self):
        left = LeftButton("left",pygame.Rect(0,MOVEBUTTON_HEIGHT+5,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),LeftButton.clicked, self)
        right = RightButton("right",pygame.Rect(MOVEBUTTON_WIDTH+5,MOVEBUTTON_HEIGHT+5,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),RightButton.clicked, self)
        up = UpButton("up",pygame.Rect(0,0,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),UpButton.clicked, self)
        down = DownButton("down",pygame.Rect(MOVEBUTTON_WIDTH+5,0,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),DownButton.clicked, self)
        self.commands = []
        buttons = [up,down,left,right]
        self.robot = Robot(200,200,100,100, "Robot", GREEN)
        self.actors = [self.robot]
        Screen.__init__(self,buttons,self.actors,BLACK)

    def addCommand(self, im, xMove, yMove):
        xPos = MOVEBUTTON_WIDTH*2+10 + len(self.commands)*(50+5)
        command = Command(self.robot, im, xMove, yMove, pygame.Rect(xPos,0,50,75), "command"+str(xPos))
        self.commands.append(command)
        self.actors.append(command)
        print self.actors