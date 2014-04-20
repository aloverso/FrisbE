import sys

sys.path.append("../")
sys.path.append("./")

import pygame
import planes
from collections import deque
from screen import Screen
from screen import Button


"""This is mostly based off of Raagini's screen
as they are very similar.  Work still needed"""

class tools(planes.Plane):

	def __init__(self, name, rect):
		planes.Plane.__init__(self, name, rect, draggable = False, grab = False)
		self.image.fill((255, 0, 0))
		self.Xpos = rect.x
		self.Ypos = rect.y
		self.name = name
		self.description = description
		"""self.image = load_my_image"""

	def clicked(self, button_name):
		self.image.fill((0,255,0))

class toolStorage(planes.Plane):

	def __init__(self, rect, draggable = False, grab = False):
		planes.Plane.__init__(self, rect, draggable, grab)
		self.image.fill((0,0,255))
		self.Xpos = rect.x
		self.Ypos = rect.y
		self.rect = rect
		"""self.image =load_my_image"""

	def inStorage(self, planes, coordinates):
		planes.Plane.inStorage(self, planes, coordinates)
		plane.moving = False

class targetZone(planes.Plane):
	def __init__(self, button_name, rect):
		planes.Plane.__init__(self, button_name, rect, draggable = False, grab = False)
		self.image.fill((0,0,255))
		self.Xpos = rect.x
		self.Ypos = rect.y
		self.rect = rect
		"""self.image - load_my_image"""

	def hitTarget(self, planes, coordinates, Button):
		planes.Plane.hitTarget(self, planes, coordinates)
		plane.moving = False
		self.image.fill((0,0,255))


class targetDisplay(planes.Display):
    def hitTarget(self, plane, coordinates):
         if isinstance(plane, tools):
             planes.Display.hitTarget(self, plane, (plane.Xpos, plane.Ypos))

class primaryScreen(Screen):
    def __init__(self):
        targ1 = targetZone("targ1", pygame.Rect(0, 0, 100, 100))
        targ2 = targetZone("targ2", pygame.Rect(450,300, 100,100))
        self.targetZones = [targ1,targ2]
        self.tools = []
        self.actors = self.targetZones + self.tools
        Screen.__init__(self, [], self.actors, (0,128,0))
