import pygame
import math
from pygame.locals import *
import random
import time
from abc import ABCMeta, abstractmethod
import planes
from planes import Plane
import planes.gui


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

class Button(planes.gui.Button):
	def __init__(self, label, rect, callback, model):
		planes.gui.Button.__init__(self, label, rect, callback)
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
        self.name = name
        self.rect = rect
        self.Xpos = self.rect.x
        self.Ypos = self.rect.y

    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, coordinates)
       plane.moving = False