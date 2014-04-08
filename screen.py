import pygame
import math
from pygame.locals import *
import random
import time
from abc import ABCMeta, abstractmethod
import planes
from planes import Plane
import planes.gui

class Screen:
	def __init__(self, title, buttons, actors):
		self.buttons = buttons
		self.actors = actors
		self.title = title

	def update(self):
		for actor in self.actors:
			actor.update()


