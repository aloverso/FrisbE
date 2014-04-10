#!/usr/bin/python3

"""Square clicking using planes

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   Based on a pure PyGame implementation
"""

# This file is part of planes.
#
# planes is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# planes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with planes.  If not, see <http://www.gnu.org/licenses/>.

# work started on 03. Oct 2010

import sys

# Add current and parent directory. One of them is supposed to contain the
# planes package.
#
sys.path.append("../")
sys.path.append("./")

import pygame
import planes
from collections import deque
from screen import Screen
from screen import Button

class Material(planes.Plane):

    def __init__(self, name, rect, draggable = True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.image.fill((255, 0, 0))
        self.Xpos = rect.x
        self.Ypos = rect.y
        self.name = name
        self.strength = 0
        self.meltingPoint = 0

    def clicked(self, button_name):
        self.image.fill((255,0,0))

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

class DropDisplay(planes.Display):
    def dropped_upon(self, plane, coordinates):
         if isinstance(plane, Material):
             planes.Display.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))

class MixingScreen(Screen):
    def __init__(self):
        drop1 = DropZone("drop1", pygame.Rect(0, 0, 100, 100))
        drop2 = DropZone("drop2", pygame.Rect(450,300, 100,100))
        self.materials = []
        for i in range(0,4):
            self.materials.append(Material("mat"+str(i), pygame.Rect((400, 600/(len(self.materials)+1) * i, 20, 20))))
        self.dropZones = [drop1,drop2]
        self.actors = self.dropZones + self.materials
        Screen.__init__(self, [], self.actors, (0,128,0))

