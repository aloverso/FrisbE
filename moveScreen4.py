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


scrleft = 50
scrright = 1150
scrtop = 50
scrbottom = 700


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class UpButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("img/up_button.png")
    def clicked(self, button_name):
        if not self.model.runClicked:
            self.model.addCommand("img/up_command.png", 0, -1)

class DownButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("img/down_button.png")
    def clicked(self, button_name):
        if not self.model.runClicked:
            self.model.addCommand("img/down_command.png", 0, 1)

class LeftButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("img/left_button.png")
    def clicked(self, button_name):
        if not self.model.runClicked:
            self.model.addCommand("img/left_command.png", -1, 0)

class RightButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("img/right_button.png")
    def clicked(self, button_name):
        if not self.model.runClicked:
            self.model.addCommand("img/right_command.png", 1, 0)

class ClearButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("img/clear_button.png")
    def clicked(self, button_name):
        if not self.model.runClicked:
            self.model.clearCommands()

class BackButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("img/delete_button.png")
    def clicked(self, button_name):
        if len(self.model.commands) > 0 and not self.model.runClicked:
            commandToRemove = self.model.commands[len(self.model.commands)-1]
            commandToRemove.image.fill(BLACK)
            self.model.commands = self.model.commands[:len(self.model.commands)-1]

class RunButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.im = pygame.image.load("img/run_button.png")
    def clicked(self, button_name):
        self.model.runClicked = True

class BuildButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image = pygame.image.load("img/back_button_med.png")
    def clicked(self, button_name):
        if not self.model.won:
            self.model.robot.money -= self.model.moneyCollected
        self.model.game.currentscreen = self.model.game.buildscreen
        self.model.robot.setPosition(self.model.game.buildscreen.startPosition[0], self.model.game.buildscreen.startPosition[1])

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
        self.run = RunButton("run", pygame.Rect(0, MOVEBUTTON_HEIGHT*2 + 10 + 30, 105, 45), RunButton.clicked, self)
        build = BuildButton("buildscreenbutton", pygame.Rect(WINDOWWIDTH-225, 110, 200, 50), BuildButton.clicked, self)
        self.robot = robot
        self.commands = []
        self.buttonsWithoutRun = [up,down,left,right,back,clear, build]
        self.runClicked = False

        if self.robot.level == 1:
            level = levels.Level1()
        elif self.robot.level ==2:
            level = levels.Level2()
        elif self.robot.level ==3:
            level = levels.Level3()
        #elif self.robot.level ==4:
        #    level = levels.Level4()
        else:
            level = levels.Level3()

        self.startPosition = (level.start[0] - self.robot.width, level.start[1] - self.robot.height)
        self.notificationCreationTime = 0
        self.notification = None

        self.walls = level.walls
        self.goal = level.goal
        self.money = level.money
        self.won = False
        self.runningThisScreen = False
        self.moneyCollected = 0

        self.startTime = 0
        font1 = pygame.font.SysFont("Arial", 40)
        self.moneyLabel = ScreenText("moneytext", "Money: "+str(self.robot.money), pygame.Rect(WINDOWWIDTH-225, 0, 200, 50), font1)
        self.timeLabel = ScreenText("timetext", "Time: "+str((pygame.time.get_ticks() - self.startTime)/1000.0), pygame.Rect(WINDOWWIDTH-225,55,200,50), font1)
        self.timeLabel.updateColor((100,100,255))
        self.actorsWithoutNotification = self.walls + self.money + [self.timeLabel, self.moneyLabel,self.robot]
        self.actors = self.actorsWithoutNotification
        Screen.__init__(self,self.buttonsWithoutRun,self.actors,BLACK)

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
            command = Command(self.robot, im, self.robot.width*xMove, self.robot.height*yMove, pygame.Rect(xPos,yPos,50,75), "command"+str(xPos)+str(yPos))
            self.commands.append(command)
            self.actors.append(command)

    def runCommands(self, command):
        command.beingRun()
        newRobotRect = pygame.Rect(self.robot.rect.x + command.xMove, self.robot.rect.y + command.yMove, self.robot.rect.width, self.robot.rect.height)
        canMove = True
        for coin in self.money:
            if newRobotRect.colliderect(coin.rect):
                self.robot.money += coin.value
                self.moneyCollected += coin.value
                coin.fill()
                coin = None

        for wall in self.walls:
            if newRobotRect.colliderect(wall.rect):
                canMove = False
        if newRobotRect.x + self.robot.width > WINDOWWIDTH or newRobotRect.x < 0 or newRobotRect.y + self.robot.height > WINDOWHEIGHT:
            canMove = False
        self.robot.move(command.xMove, command.yMove)

        #TEST IF YOU WON!
        if not canMove and newRobotRect.colliderect(self.goal):
            self.clearCommands()
            font2 = pygame.font.SysFont("Arial", 30)
            timeElapsed = (pygame.time.get_ticks() - self.startTime)/1000
            winnings = 3000/timeElapsed
            self.robot.money += winnings
            wn1 = ScreenText("wn1", "Level "+str(self.robot.level)+" Complete!", pygame.Rect(WINDOWWIDTH/2- 150, WINDOWHEIGHT/8 + 100, 300,50), font2)
            wn2 = ScreenText("wn2", "Total Time: "+str(timeElapsed), pygame.Rect(WINDOWWIDTH/2 - 150, WINDOWHEIGHT/8 + 150, 300, 50), font2)
            wn3 = ScreenText("wn3", "Time Bonus: "+ str(winnings),pygame.Rect(WINDOWWIDTH/2 - 150, WINDOWHEIGHT/8 + 200, 300, 50), font2)
            wn4 = ScreenText("wn4", "Money Collected: "+ str(self.moneyCollected),pygame.Rect(WINDOWWIDTH/2 - 150, WINDOWHEIGHT/8 + 250, 300, 50), font2)
            wn5 = ScreenText("wn5", "Your Total Money: "+str(self.robot.money),pygame.Rect(WINDOWWIDTH/2 - 150, WINDOWHEIGHT/8 + 300, 300, 50), font2)
            winbox = planes.Plane("winbox", pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8,3*WINDOWWIDTH/4,3*WINDOWHEIGHT/4))
            winbox.image = pygame.image.load("img/win_notification_box.png")
            win_array = [winbox, wn1,wn2,wn3,wn4,wn5]
            self.actors += win_array
            toBuildScreen = BuildButton("tobuildscreen", pygame.Rect(WINDOWWIDTH/2-100, 3*WINDOWHEIGHT/4, 200,50), BuildButton.clicked, self)
            self.buttons.append(toBuildScreen)
            self.robot.level += 1
            self.won = True

        #did you hit a wall?

        elif not canMove:
            self.clearCommands()
            font3 = pygame.font.SysFont("Arial", 14)
            self.notificationCreationTime = pygame.time.get_ticks()
            self.notification = ScreenText("hitwall", "Wall Hit! "+str(self.robot.bumper)+"-second penalty", pygame.Rect(WINDOWWIDTH-225,165,200,50), font3)
            self.notification.updateColor((255,0,0))
            self.startTime -= 10000
            self.actors.append(self.notification)
            self.robot.move(command.xMove*-1, command.yMove*-1)
        command.doneRunning()
        time.sleep(self.robot.motorspeed)

    def clearCommands(self):
        for command in self.commands:
            command.image.fill(BLACK)
        self.commands = []

    def update(self):
        if len(self.commands) >= 10:
            self.run.image = pygame.image.load("img/run_button.png")
            self.buttons.append(self.run)
        else:
            self.run.image.fill(BLACK)
            self.buttons = self.buttonsWithoutRun
        if not self.runningThisScreen:
            self.runningThisScreen = True
            self.startTime = pygame.time.get_ticks()
        self.timeLabel.updateText("Time: " + str((pygame.time.get_ticks() - self.startTime)/1000))
        self.moneyLabel.updateText("Money: "+str(self.robot.money))
        if self.runClicked:
            self.run.image.fill(BLACK)
            self.buttons = self.buttonsWithoutRun
            if len(self.commands) > 0:
                self.runCommands(self.commands[0])
                self.commands = self.commands[1:]
            else:
                self.runClicked = False
        if self.notificationCreationTime > 0:
            if pygame.time.get_ticks() - self.notificationCreationTime >= 3000:
                self.notification.image.fill(BLACK)
                self.actors = self.actorsWithoutNotification
                self.notificationCreationTime = 0
