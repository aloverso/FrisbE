import pygame
import math
from pygame.locals import *
import random
import time
from abc import ABCMeta, abstractmethod
import planes
from planes import Plane
import planes.gui
from planes import *


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
		planes.Plane.__init__(self,label,rect,draggable=False, grab=False)
		self.image.fill(WHITE)
		self.rect = rect
		self.model = model
	def update(self):
		pass

class DropZone(planes.Plane):
    def __init__(self, name, rect):
        planes.Plane.__init__(self, name, rect, draggable = False, grab = True)
        self.name = name
        self.image.fill((0,0,255))
        self.rect = rect
        self.Xpos = self.rect.x
        self.Ypos = self.rect.y
        self.thingsDroppedOnMe = []

    def dropped_upon(self, plane, coordinates):
        planes.Plane.dropped_upon(self, plane, (coordinates[0]+self.Xpos, coordinates[1]+self.Ypos))
        plane.moving = False
      	self.thingsDroppedOnMe.append(plane)

class DropDisplay(planes.Display):
    def dropped_upon(self, plane, coordinates):
         if isinstance(plane, planes.Plane):
             planes.Display.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))

class ScreenText(gui.Label):
	def __init__(self,name,text,rect,font):
		planes.Plane.__init__(self,name,rect,draggable=False, grab=False)

		if self.name.startswith("infoText") or self.name.startswith("text"):
			self.background_color = BLACK
			self.text_color = WHITE
		else:
			self.background_color = (0,0,0,0)
			self.text_color = WHITE

		gui.Label.__init__(self,name,text,rect,self.background_color, self.text_color, font)


		#planes.gui.Label.__init__(self,name,text,rect,self.background_color, WHITE, font)

		# font is declared as the following: fontname (or whatever you call it) = pygame.font.SysFont("Arial", 40)
		# it takes the font (Arial) and fontsize (40)
		# we should stick to Arial probably because pygame doesn't support many fonts and it looks nice
		# change your font size as needed
	
	def updateText(self, text):
		self.text = text

	def updateColor(self, color):
		#print color
		self.text_color = color

	def updateBackground(self, color):
		self.background_color = color

"""
LABELS

text_color - why does it not change?  or only sometimes?

background_color = how?

line breaks - how?
"""
