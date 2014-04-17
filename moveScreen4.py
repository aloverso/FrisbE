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
from random import randint

MOVEBUTTON_HEIGHT = 75
MOVEBUTTON_WIDTH = 50


WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


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

class RunButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        self.model.runClicked = True

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
        

class Wall(planes.Plane):
    def __init__(self, name, rect):
        planes.Plane.__init__(self, name, rect, draggable=False, grab=False)
        self.image.fill(WHITE)

   
class MoveScreen(Screen):
    def __init__(self, robot, game):
        self.game = game
        left = LeftButton("left",pygame.Rect(0,MOVEBUTTON_HEIGHT+5,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),LeftButton.clicked, self)
        right = RightButton("right",pygame.Rect(MOVEBUTTON_WIDTH+5,MOVEBUTTON_HEIGHT+5,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),RightButton.clicked, self)
        up = UpButton("up",pygame.Rect(0,0,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),UpButton.clicked, self)
        down = DownButton("down",pygame.Rect(MOVEBUTTON_WIDTH+5,0,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),DownButton.clicked, self)
        back = BackButton("back", pygame.Rect(0, MOVEBUTTON_HEIGHT*2 + 10,MOVEBUTTON_WIDTH, 25),BackButton.clicked, self)
        clear = ClearButton("clear", pygame.Rect(MOVEBUTTON_WIDTH+5, MOVEBUTTON_HEIGHT*2 + 10, MOVEBUTTON_WIDTH, 25),ClearButton.clicked, self)
        run = RunButton("run", pygame.Rect(0, MOVEBUTTON_HEIGHT*2 + 10 + 30, MOVEBUTTON_WIDTH*2 + 5, 25), RunButton.clicked, self)
        self.robot = robot
        self.commands = []
        buttons = [up,down,left,right,back,clear,run]
        self.actors = [self.robot]
        Screen.__init__(self,buttons,self.actors,BLACK)
        self.runClicked = False
        """
        numWalls = randint(2*(self.robot.level+1),(WINDOWWIDTH*WINDOWHEIGHT)/(self.robot.width*self.robot.height))
        for i in range(numWalls):
            x = randint(0, WINDOWWIDTH/self.robot.width)*self.robot.width
            y = randint(0, WINDOWHEIGHT/self.robot.height)*self.robot.height
            self.actors.append(Wall("wall"+str(i), pygame.Rect(x,y,self.robot.width,self.robot.height)))
        """

    def addCommand(self, im, xMove, yMove):
        xPos = MOVEBUTTON_WIDTH*2+10 + len(self.commands)*(50+5)
        command = Command(self.robot, im, xMove, yMove, pygame.Rect(xPos,0,50,75), "command"+str(xPos))
        self.commands.append(command)
        self.actors.append(command)

    def runCommands(self, command):
        command.beingRun()
        self.robot.move(command.xMove, command.yMove)
        command.doneRunning()
        time.sleep(.5)

    def update(self):
        for actor in self.actors:
            actor.update
        if self.runClicked:
            if len(self.commands) > 0:
                self.runCommands(self.commands[0])
                self.commands = self.commands[1:]
            else:
                self.runClicked = False



 
"""
BUGS:
- clear and back work logically but don' remove the icons from the screen
- run commands isn't going discretely

"""

