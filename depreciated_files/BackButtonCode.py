        



        #This goes in your screen (pseudomodel) class in the init method
        buttonback = BackButton("back", "ray.jpg", pygame.Rect(8*WINDOWWIDTH/10, 9*WINDOWHEIGHT/10, 2*WINDOWWIDTH/10, WINDOWHEIGHT/10), BackButton.clicked, self)
        self.buttons.append(buttonback)


#This goes with the buttons in your game, its just a separate class
class BackButton(Button):
    def __init__(self, label, im, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.image.fill((0,0,255))
    def clicked(self, button_name):
        self.model.gamemodel.currentscreen = self.model.gamemodel.homescreen 