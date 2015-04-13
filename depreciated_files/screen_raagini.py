import pygame
import math

from pygame.locals import *
import random
import time
from abc import ABCMeta, abstractmethod
from planes import *
#import planes

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Screen:
	def __init__(self, buttons, actors, background):
		self.buttons = buttons
		self.actors = actors
		self.background = background

	def update(self):
		for actor in self.actors:
			actor.update()

class Button(gui.Button):
	def __init__(self, label, rect, callback, model):
		gui.Button.__init__(self, label, rect, callback)
		Plane.__init__(self,label,rect,draggable=False, grab=False)
		self.image.fill(WHITE)
		self.rect = rect
		self.model = model
	def update(self):
		pass

class ScreenText(gui.Label):
    def __init__(self,name,text,rect,font):

        Plane.__init__(self,name,rect,draggable=False, grab=False)
        
        if self.name.startswith("text") or self.name.startswith("infoText"):
            background_color = (0,0,0)
            text_color = WHITE
        else:
            background_color = (0,0,0,0)
            text_color = BLACK
        
        self.font = pygame.font.SysFont("Arial", 40)       
        gui.Label.__init__(self,name,text,rect,background_color, text_color)
        
       
        self.font = pygame.font.SysFont("Arial", 40)
        
        # font is declared as the following: fontname (or whatever you call it) = pygame.font.SysFont("Arial", 40)
        # it takes the font (Arial) and fontsize (40)
        # we should stick to Arial probably because pygame doesn't support many fonts and it looks nice
        # change your font size as needed
    
    def updateText(self, text):
        self.text = text


class DropDisplay(Display):
    def dropped_upon(self, plane, coordinates):
         if isinstance(plane, planes.Plane):
            Display.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))
                          
class DropZone(Plane):
    def __init__(self, name, rect):
        Plane.__init__(self, name, rect, draggable = False, grab = True)
        self.name = name
        self.image.fill((0,0,255))
        self.name = name
        self.rect = rect
        self.Xpos = self.rect.x
        self.Ypos = self.rect.y

    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))
       plane.moving = False
