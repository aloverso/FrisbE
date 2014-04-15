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

MOVEBUTTON_HEIGHT = 75
MOVEBUTTON_WIDTH = 50

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Robot(planes.Plane):
    def __init__(self, name, rect, im):
        planes.Plane.__init__(self, name, rect, draggable=False, grab=False)
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height
        self.vx = 0.0
        self.vy = 0.0
        self.level = 1
        self.money = 100
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
        self.model.addCommand("up.png", 0, -1)

class DownButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("down.png")
    def clicked(self, button_name):
        self.model.addCommand("down.png", 0, 1)

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

class ClearButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        self.model.commands = []

class BackButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        commandToRemove = self.model.commands[len(self.model.commands)-1]
        commandToRemove.remove(self)


        self.model.commands = self.model.commands[:len(self.model.commands)-1]
        print self.model.commands

class RunButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        self.model.runCommands()

class Command(planes.Plane):
    def __init__(self, robot, im, xMove, yMove, rect, name):
        planes.Plane.__init__(self, name, rect, draggable=False, grab=False)
        self.image = pygame.image.load(im)
        self.im = im
        self.xMove = xMove
        self.yMove = yMove
        self.robot = robot
    def update(self):
        pass
    def beingRun(self):
        self.image.fill(GREEN)
    def doneRunning(self):
        #self.image = pygame.image.load(self.im)
        #self.destroy()
        pass
   
class MoveScreen(Screen):
    def __init__(self):
        left = LeftButton("left",pygame.Rect(0,MOVEBUTTON_HEIGHT+5,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),LeftButton.clicked, self)
        right = RightButton("right",pygame.Rect(MOVEBUTTON_WIDTH+5,MOVEBUTTON_HEIGHT+5,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),RightButton.clicked, self)
        up = UpButton("up",pygame.Rect(0,0,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),UpButton.clicked, self)
        down = DownButton("down",pygame.Rect(MOVEBUTTON_WIDTH+5,0,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),DownButton.clicked, self)
        back = BackButton("back", pygame.Rect(0, MOVEBUTTON_HEIGHT*2 + 10,MOVEBUTTON_WIDTH, 25),BackButton.clicked, self)
        clear = ClearButton("clear", pygame.Rect(MOVEBUTTON_WIDTH+5, MOVEBUTTON_HEIGHT*2 + 10, MOVEBUTTON_WIDTH, 25),ClearButton.clicked, self)
        run = RunButton("run", pygame.Rect(0, MOVEBUTTON_HEIGHT*2 + 10 + 30, MOVEBUTTON_WIDTH*2 + 5, 25), RunButton.clicked, self)

        self.commands = []
        buttons = [up,down,left,right,back,clear,run]
        self.robot = Robot("robot", pygame.Rect(200,200,100,100), GREEN)
        self.actors = [self.robot]
        Screen.__init__(self,buttons,self.actors,BLACK)

    def addCommand(self, im, xMove, yMove):
        xPos = MOVEBUTTON_WIDTH*2+10 + len(self.commands)*(50+5)
        command = Command(self.robot, im, xMove, yMove, pygame.Rect(xPos,0,50,75), "command"+str(xPos))
        self.commands.append(command)
        self.actors.append(command)

    def runCommands(self):
        for command in self.commands:
            command.beingRun()
            self.robot.x = self.robot.x + command.xMove*10
            self.robot.y = self.robot.y + command.yMove*10
            command.doneRunning()
 
"""
BUGS:
- clear and back work logically but don' remove the icons from the screen
- run commands isn't going discretely
- how to connect

"""

