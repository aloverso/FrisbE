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
import math
from pygame.locals import *
import random
import time
from abc import ABCMeta, abstractmethod
import planes
from planes import Plane
import planes.gui

import settings_screen
import homescreen_good

WINDOWWIDTH = 600
WINDOWHEIGHT = 600

screens = [homescreen_good, settings_screen]

class Menu:

    pygame.init()
    currentScreen = screens[0]
    size = (WINDOWWIDTH,WINDOWHEIGHT)
    screen = pygame.display.set_mode(size)
    model = currentScreen.Model()
    view = currentScreen.View(model,screen)
    running = True

    screen = planes.Display((600, 600))
    screen.grab = True
    screen.image.fill((0, 128, 0))

    for actor in model.actors:
	screen.sub(actor)

    while running:

        events = pygame.event.get()

	for event in events:

		if event.type == pygame.QUIT:
		    print("got pygame.QUIT, terminating")
		    raise SystemExit

	screen.process(events)
	screen.update()
	screen.render()
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
        
if __name__ == '__main__': 
    Menu()
    
