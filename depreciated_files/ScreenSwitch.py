from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, SwapTransition, SlideTransition, NoTransition

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<ButtonWidget>:
    canvas:
        Color:
            rgb: self.r, self.g, self.b   
        Rectangle:
            pos:self.pos
            size:self.size
            
<MenuScreen>:
    FloatLayout:
        Button:
            text: 'Settings'
            on_press: root.manager.current = 'settings'
            size_hint:.5, .25
            pos:root.x, root.y
        Button:
            text: 'Games'
            on_press: root.manager.current = 'games'
            size_hint:.5, .25
            pos:root.width-self.width, root.y
        Button:
            text: 'In the Menu!'
            size_hint:.2, .2
            pos: root.center_x, root.center_y
        

<SettingsScreen>:
    FloatLayout:
        Button:
            text: 'Menu'
            on_press: root.manager.current = 'menu'
            size_hint:.5, .25
            pos:root.width-self.width, root.y
        Button:
            text: 'In the Settings!'
            size_hint:.2, .2
            pos: root.center_x, root.center_y
    
<GamesScreen>:
    FloatLayout:
        button1:MainButton
        Button:
            text: 'Menu'
            on_press: root.manager.current = 'menu'
            size_hint:.5, .25
            pos:root.x, root.y
        Button:
            text: 'In the Games!'
            size_hint:.2, .2
            pos: root.center_x, root.center_y
            on_press: root.manager.current = 'rectangles'
        Button:
            id:'MainButton

<RectangleScreen>:
    FloatLayout:
        button1: leftButton
        button2: centerButton
        button3: rightButton
        
        ButtonWidget:
            id:leftButton
            size_hint:.2, .2
            pos:root.x, root.center_y
        ButtonWidget:
            id:centerButton
            size_hint:.2, .2
            pos:root.center_x, root.center_y
        ButtonWidget:
            id:rightButton
            size_hint:.2, .2
            pos:root.width-self.width, root.center_y
        Button:
            text: 'Back'
            size_hint: .2, .2
            pos:0, root.y
            on_press: root.manager.current = 'menu'
""")

# Declare three screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class GamesScreen(Screen):
    button1 = ObjectProperty(None)

class RectangleScreen(Screen):
    pass

class ButtonWidget(Widget):
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)
    touches = 0

    def __init__(self, **kwargs):
        self.r = 1
        self.g = 0
        self.b = 0
        super(ButtonWidget, self).__init__(**kwargs)

    def red(self):
        self.r = 1.0
        self.g = 0.0
        self.b = 0.0
    def blue(self):
        self.r = 0.0
        self.g = 0.0
        self.b = 1.0
    def green(self):
        self.r = 0.0
        self.g = 1.0
        self.b = 0.0
        
    def on_touch_down(self, touch):
        colors = [1, 2, 3]
        if self.touches == 3:
            self.touches = 0        
        if self.collide_point(touch.x,touch.y):
            if colors[self.touches] == 1:
                self.red()
            if colors[self.touches] ==2:
                self.blue()
            if colors[self.touches] ==3:
                self.green()
        self.touches += 1

#Create the screen manager
sm = ScreenManager(transition=NoTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(GamesScreen(name='games'))
sm.add_widget(RectangleScreen(name = 'rectangles'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()