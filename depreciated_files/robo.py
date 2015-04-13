# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 16:58:55 2014

@author: anneubuntu
"""
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, SwapTransition, SlideTransition, NoTransition
from kivy.uix.boxlayout     import BoxLayout
from kivy.uix.button        import Button


Builder.load_string("""

<basicNav>
    
  
""")

class basicNav(ScreenManager):
    def __init__(self, screenList, **kwargs):
        super(basicNav,self).__init__(**kwargs)
        self.screenList(screenList)
        self.current = screen_list[0]
 
    def buttonReleased(self,b):
        self.current = b

class Moveable(Widget):
    pass    
    
class PongPaddle(Widget):
    score = NumericProperty(0)
    
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            
class Robot(Widget):
    shield = NumericProperty(0)
    
class Upgrade(Widget):
    pass
    
class ObstacleCourse(Widget):
    obstacles = ListProperty([]) #list of obstacles in course
    pass

class Obstacle(Widget):
    pass

class Player(Widget):
    robot = ObjectProperty(None) #the player's robot
    level = NumericProperty(0) #the player's level
    money = NumericProperty(0) #the player's cash
    inventory = ListProperty([]) #the player's purchased items. List of Upgrades


class Model(Widget):
    manager = ObjectProperty(None)
    sm = basicNav(["screen0","screen1","screen2","screen3"])
    course = ObjectProperty(None) #is an obstacle course
    level = NumericProperty(0) #what level is the player on
    player = ObjectProperty(None) #player
    
    
    
    def update(self, dt):
        pass
            
        
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
            


class PongApp(App):
    
    def build(self):
        game = Model()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game.sm
        
class PongBall(Widget):

    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


if __name__ == '__main__':
    PongApp().run()