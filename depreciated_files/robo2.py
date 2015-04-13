# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 21:02:41 2014

@author: anneubuntu
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 16:58:55 2014

@author: anneubuntu
"""
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, SwapTransition, SlideTransition, NoTransition
from kivy.uix.boxlayout     import BoxLayout
from kivy.uix.button        import Button
from kivy.uix.gridlayout     import GridLayout
from kivy.uix.stacklayout import StackLayout


Builder.load_string("""

<RoboGame>
    robot: robot

    StackLayout:
        orientation: 'bt-lr'
        Button:
            text: 'Up'
            size_hint: .5, 1
            on_press: root.commands = root.commands + self.text[0:1]
        Button:
            text: 'Down'
            size_hint: .5, 1
            on_press: root.commands = root.commands + self.text[0:1]
        Button:
            text: 'Left'
            size_hint: .5, 1
            on_press: root.commands = root.commands + self.text[0:1]
        Button:
            text: 'Right'
            size_hint: .5, 1
            on_press: root.commands = root.commands + self.text[0:1]
            
    FloatLayout:
        Button:
            text: 'Run'
            size_hint:.5, .25
            pos: root.x, root.y+100
            on_press: root.scheduledRun()
        Button:
            text: 'Back'
            size: 100, 50
            pos: root.x+100, root.y+100
            on_press: root.commands = root.commands[:len(root.commands)-1]
        Button:
            text: 'Clear'
            size: 100, 50
            pos: root.x+100, root.y+150
            on_press: root.commands = ''
    
    Label:
        font_size: 70
        right: 320
        top: root.y + 100
        text: root.commands
        
    Robot:
        id: robot
        center_x: root.center_x
        center_y: root.center_y
        
<Robot>
    size: 100,100
    canvas:
        Rectangle:
            pos: self.pos
            size: self.size
  
""")
        

class Robot(Widget):
    
    def move(self, x, y):
        self.pos = self.x + x, self.y + y
        print "i moved"
    

class RoboGame(Widget):
    robot = ObjectProperty(None)
    commands = StringProperty('')
    
    def scheduledRun(self):
        l = len(self.commands)
        for i in range(l):
            Clock.schedule_once(self.run, i)
            self.commands = self.commands[1:]
        self.commands = ''

    def run(self, dt):
        print "running"
        x = 0
        y = 0
        c = self.commands[0:1]
        if c == "U":
            y = 10
        elif c=="D":
            y = -10
        elif c=="L":
            x = -10
        elif c=="R":
            x = 10
        self.robot.move(x,y)
        
    def runAll(self):
        x = 0
        y = 0
        for c in self.commands:
            if c == "U":
                y = 10
            elif c=="D":
                y = -10
            elif c=="L":
                x = -10
            elif c=="R":
                x = 10
            self.robot.move(x,y)
        self.commands = ''

    def update(self, dt):
        self.robot.move()
        
class RoboApp(App):
    def build(self):    
        game = RoboGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game
        
if __name__ == '__main__':
    RoboApp().run()