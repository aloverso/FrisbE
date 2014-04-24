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
import levels
from screen import ScreenText

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
        if not self.model.runClicked:
            self.model.addCommand("up.png", 0, -1)

class DownButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("down.png")
    def clicked(self, button_name):
        if not self.model.runClicked:
            self.model.addCommand("down.png", 0, 1)

class LeftButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("left.png")
    def clicked(self, button_name):
        if not self.model.runClicked:
            self.model.addCommand("left.png", -1, 0)

class RightButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("right.png")
    def clicked(self, button_name):
        if not self.model.runClicked:
            self.model.addCommand("right.png", 1, 0)

class ClearButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        if not self.model.runClicked:
            self.model.clearCommands()

class BackButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        if not self.model.runClicked:
            commandToRemove = self.model.commands[len(self.model.commands)-1]
            commandToRemove.image.fill(BLACK)
            self.model.commands = self.model.commands[:len(self.model.commands)-1]

class RunButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
    def clicked(self, button_name):
        self.model.runClicked = True

class Command(planes.Plane):
    def __init__(self, robot, im, xMove, yMove, rect, name):
        planes.Plane.__init__(self, name, rect, draggable=False, grab=False)
        if isinstance(im,tuple):
            self.image.fill(im)
        else:
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
        self.image.fill(BLACK)
   
class MoveScreen(Screen):
    def __init__(self, robot, game):
        self.game = game
        left = LeftButton("left",pygame.Rect(0,MOVEBUTTON_HEIGHT+5,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),LeftButton.clicked, self)
        right = RightButton("right",pygame.Rect(MOVEBUTTON_WIDTH+5,MOVEBUTTON_HEIGHT+5,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),RightButton.clicked, self)
        up = UpButton("up",pygame.Rect(0,0,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),UpButton.clicked, self)
        down = DownButton("down",pygame.Rect(MOVEBUTTON_WIDTH+5,0,MOVEBUTTON_WIDTH,MOVEBUTTON_HEIGHT),DownButton.clicked, self)
        back = BackButton("back", pygame.Rect(0, MOVEBUTTON_HEIGHT*2 + 10,MOVEBUTTON_WIDTH, 25),BackButton.clicked, self)
        clear = ClearButton("clear", pygame.Rect(MOVEBUTTON_WIDTH+5, MOVEBUTTON_HEIGHT*2 + 10, MOVEBUTTON_WIDTH, 25),ClearButton.clicked, self)
        run = RunButton("run", pygame.Rect(0, MOVEBUTTON_HEIGHT*2 + 10 + 30, MOVEBUTTON_WIDTH*2 + 5, 45), RunButton.clicked, self)
        self.robot = robot
        self.commands = []
        self.actors = []
        buttons = [up,down,left,right,back,clear,run]
        Screen.__init__(self,buttons,self.actors,BLACK)
        self.runClicked = False
        self.startPosition = (levels.level1start[0]-self.robot.width, levels.level1start[1]-self.robot.height)

        if self.robot.level == 1:
            self.walls = levels.level1walls
            self.goal = levels.level1goal
            self.money = levels.level1money
            self.actors = self.actors + self.walls + self.money

        self.actors.append(self.robot)
        self.runningThisScreen = False

        self.startTime = 0
        font1 = pygame.font.SysFont("Arial", 40)
        self.timeLabel = ScreenText("timetext", "Time: "+str((pygame.time.get_ticks() - self.startTime)/1000.0), pygame.Rect(WINDOWWIDTH-225,0,200,50), font1)
        self.actors.append(self.timeLabel)
        """
        for i in range(60):
            self.addCommand(GREEN, 0, 0)
        
        numWalls = randint(2*(self.robot.level+1),(WINDOWWIDTH*WINDOWHEIGHT)/(self.robot.width*self.robot.height))
        for i in range(numWalls):
            x = randint(0, WINDOWWIDTH/self.robot.width)*self.robot.width
            y = randint(0, WINDOWHEIGHT/self.robot.height)*self.robot.height
            self.actors.append(Wall("wall"+str(i), pygame.Rect(x,y,self.robot.width,self.robot.height)))
        """

    def addCommand(self, im, xMove, yMove):
        if len(self.commands) != 0:
            yPos = self.commands[len(self.commands)-1].rect.y
            xPos = self.commands[len(self.commands)-1].rect.x + MOVEBUTTON_WIDTH + 5
        else:
            yPos = 0
            xPos = MOVEBUTTON_WIDTH*2+10
        if xPos+MOVEBUTTON_WIDTH > WINDOWWIDTH-250:
            xPos = MOVEBUTTON_WIDTH*2+10
            yPos = yPos + MOVEBUTTON_HEIGHT + 5
        if yPos < 3 * MOVEBUTTON_HEIGHT:
            command = Command(self.robot, im, xMove, yMove, pygame.Rect(xPos,yPos,50,75), "command"+str(xPos)+str(yPos))
            self.commands.append(command)
            self.actors.append(command)

    def runCommands(self, command):
        command.beingRun()
        newRobotRect = pygame.Rect(self.robot.rect.x + command.xMove, self.robot.rect.y + command.yMove, self.robot.rect.width, self.robot.rect.height)
        canMove = True
        for coin in self.money:
            if newRobotRect.colliderect(coin.rect):
                self.robot.money += coin.value
                coin.fill()
                self.money.remove(coin)
        for wall in self.walls:
            if newRobotRect.colliderect(wall.rect):
                canMove = False
        if newRobotRect.x + self.robot.width > WINDOWWIDTH or newRobotRect.x < 0 or newRobotRect.y + self.robot.height > WINDOWHEIGHT:
            canMove = False
        if canMove:
            self.robot.move(command.xMove, command.yMove)
        elif newRobotRect.colliderect(self.goal):
            print self.robot.money
            timeElapsed = (pygame.time.get_ticks() - self.startTime)/1000
            self.robot.money += 1000.0/timeElapsed
            print timeElapsed
            print self.robot.money
        else:
            self.clearCommands()
            self.robot.setPosition(self.startPosition[0], self.startPosition[1])
        command.doneRunning()
        time.sleep(self.robot.motorspeed)

    def clearCommands(self):
        for command in self.commands:
            command.image.fill(BLACK)
        self.commands = []

    def update(self):
        if not self.runningThisScreen:
            self.runningThisScreen = True
            self.startTime = pygame.time.get_ticks()
        self.timeLabel.updateText("Time: " + str((pygame.time.get_ticks() - self.startTime)/1000))
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
- how labels?
- coin removal on 2

**ADD DA MOTOR ROBOT SHIT
"""

