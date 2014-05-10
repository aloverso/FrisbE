import pygame
import planes
from collections import deque
from screen import Screen
from screen import Button
from screen import DropZone

WINDOWWIDTH = 1200
WINDOWHEIGHT = 750

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Tools(planes.Plane):
	def __init__(self, name, rect,im, draggable = True,grab = True):
		planes.Plane.__init__(self, name, rect, draggable, grab)
		self.image = pygame.image.load(im)



    def clicked(self, button_name):
        self.image.fill((255,0,0))

class Parts(planes.Plane):
	def __init__(self, name, rect,im, draggable = True, grab = True):
		planes.Plane.__init__(self, name, rect, draggable, grab)
		self.im = pygame.image.load(im)

	def clicked(self, button_name):
		self.image.fill((255,0,0))

class 

class InformationScreen(Screen):
	def __init__(self,Tools,Parts):
		self.game = game
		self.Tools = Tools
		self.Parts = Parts
		self.actors = []
