"""
===
How to make a Game for our Screen Switcher
===

There is no "Game" class you need to extend from because games are just a structure to hold and organize code.
Take a look at this example game class:
"""

class RoboGame: # again, doesn't extend anything
	def __init__(self): # nothing needed in the constructor.  Every aspect of a game is defined within the game itself

		self.robot = Robot("robot", pygame.Rect(200,200,100,100), GREEN) 	# this game needs a robot that is on every screen of the game.
																			# Therefore, I added a robot class declared in the same script as this
																			# made a single robot here that is a property of the game
																			# and it gets passed into each screen instance within the game
																			# so the screens can access it or change it's location as they need
		
		self.buildscreen =  BuildScreen(self.robot,self) 	# these are declaring screens within the game
															# they'll vary depending on how many screens you need
															# passing the self.robot into the screen is something this game does, not
															# every game will need to
															# passing "self" - i.e. passing THIS GAME into the screen is very important
															# the screen will contain buttons that might cause screen switching
															# in order to do that, the button's "clicked" method will have to set the 
															# game's current screen, so it needs to "know" what game it comes from
															# more on this later
		self.movescreen = MoveScreen(self.robot,self)
		self.storescreen = StoreScreen(self.robot, self)

		# this bit should be in all the game screens.  it creates three title screens that all games need to have
		# you'll notice that in the button declarations, the button width is set to 3/4 of the window width
		# but when you run the code, the buttons only go like halfway across the screen
		# this is because we're using the startbut.png image to represent the button, and the image is smaller than our button size
		# the button is still there on the other half of the screen (try clicking it) but it doesn't have a graphic
		# we can easily fix this by fixing the graphics
		start = StartButton("start","startbut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),StartButton.clicked, self)
		settings = SettingsButton("settings","setbut.png",pygame.Rect(WINDOWWIDTH/8,6*WINDOWHEIGHT/8 + 30,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),SettingsButton.clicked, self)
		tutorial = TutorialButton("tutorial","tutbut.png",pygame.Rect(WINDOWWIDTH/8,5*WINDOWHEIGHT/8 + 20,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),TutorialButton.clicked, self)
		home = HomeButton("home","homebut.png",pygame.Rect(WINDOWWIDTH/8,4*WINDOWHEIGHT/8 + 10,3*WINDOWWIDTH/4,WINDOWHEIGHT/8),HomeButton.clicked, self)
		tr = pygame.Rect(WINDOWWIDTH/8, WINDOWHEIGHT/8, 3*WINDOWWIDTH/4, 3*WINDOWHEIGHT/8)
		self.homescreen = Screen([start,settings,tutorial],[titleRect("home.png",tr,WHITE)],BLACK)
		self.settingsscreen = Screen([home,settings,tutorial],[titleRect("settings.png",tr,WHITE)],BLACK)
		self.tutorialscreen = Screen([home,settings, tutorial],[titleRect("tut.png",tr,WHITE)],BLACK)

		#this is really important, again in all screens
		# you need to have a current screen called "currentscreen" so that the model in ScreenSwitcher is able to set IT'S current screen 
		# to the current screen of the game it's running
		# this is a bit confusing because in the games it's called "currentscreen" and in the Model it's called "currentScreen" but it works
		self.currentscreen = self.homescreen

"""
How to make a screen for your game
"""
class BuildScreen(Screen): # every screen will extend the Screen class
    def __init__(self, robot, game): 	# the robot bit is just for this game.  But EVERY screen should have a game passed into it
    									# that's the "self" that we passed into it in the Game definition
        self.robot = robot
        self.game = game # need this!!!

        # this is adding buttons to the screen.  The StoreButton and such are all defined classes within this script
        store = StoreButton("storebutton", pygame.Rect(0, WINDOWHEIGHT-50, 75, 50), StoreButton.clicked, self)
        start = StartButton("movescreen", pygame.Rect(WINDOWWIDTH-75, WINDOWHEIGHT-50, 75, 50), StartButton.clicked, self)
        add = AddButton("add", pygame.Rect(500, 0, 75, 50), AddButton.clicked, self)
        upgrade1 = Upgrade("u1", pygame.Rect(0,0,50,50), BLUE, 20)
        buttons = [start, store, add]
        self.actors = [robot,upgrade1]
        # every screen takes a list of actors (things that appear on the screen) and buttons
        # the BLACK is the background of the screen.  This is included to make it easy to change the screen backgrounds to pictures if we want
        Screen.__init__(self,buttons,self.actors,BLACK)

# every screen needs to have an update function, which gets called in this code here, which is in the Running loop in Screen Switcher
		if model.inGame:
			model.currentGame.currentscreen.update()
			model.currentScreen = model.currentGame.currentscreen
# luckily, the Screen class itself has an update function, so you don't need to add one unless you need to overwrite it and your screen needs
# to do something special when it updates, for example:
# this is the update function for my MoveScreen. 

    def update(self):
        for actor in self.actors: 	# this line and
            actor.update 		 	# this line are the normal Screen update and should happen in case any of your actors need updating
            						# right now none of my actors do but in case you do, it's good to have
        
        if self.runClicked:			# this is the bit that's different, and it's what lets me run my robot commands discretely instead of all at once
        							# just an example of how a screen might need to change what it does each loop
            if len(self.commands) > 0:
                self.runCommands(self.commands[0])
                self.commands = self.commands[1:]
            else:
                self.runClicked = False

 # let's go back to the Screen Switcher code real quick

 		if model.inGame:	# when you click one of those four buttons on the dashboard to enter a game, this is set as true
 							# that's so that the Model knows to use the game's currentscreen as the Model's current screen
 							# instead of the Model's dashboard screen

			model.currentGame.currentscreen.update() # this is why each screen needs an update method
			model.currentScreen = model.currentGame.currentscreen 	# this is why every game needs to have a currentscreen
																	# this is what sets the Model's currentScreen (which is the
																	# screen that the View draws) to the right game screen

"""
But how do you change the gamescreen in your game?
"""

# answer: With buttons!
# this is the Start Button code that shows up in the Title Screen stuffs that I told you to copy pasta to make title screens in all your games
"""I WAS A BIT WRONG AND YOU'RE GONNA HAVE TO CHANGE THIS CODE!"""
# take a look-see:

class StartButton(Button): # obviously all buttons should extend Button, which is a class in screen.py you may have to import
	def __init__(self, label, im, rect, callback, model):	# a couple things are going on here:
															# label: all buttons need a name. Basically all planes do
															# WARNING: all your names need to be DIFFERENT or else one will overwrite the other
															# like, if you had two different buttons declared and they both had name "button"
															# then you'd end up sad because only one would show up

															# im - startbutton has an image associated with it.
															# eventually all buttons will have images
															# if you DON'T want to do the trouble of making an image for your button yet
															# (totes understandable) then you just pass a color in for this parameter
															# and change the self.image command as specified below

															# rect: the pygame.Rect stuff of this guy.  Straightforward

															# callbacK: the function this calls when it's clicked.  This should be
															# <ButtonName>.clicked.  So when I'm declaring this button it's callback is
															# StartButton.clicked and notice NO () after the "clicked"!

															# model: this is a bit of a misnomer, because the "model" we're passing in here
															# is NOT the Model in Screen Switcher but in fact the model that the button is in
															# so because this startbutton is declared in my RoboGame class
															# when I pass in "self" as the model to the button, it's passing the Game
															# this is what lets the button switch screens
															# so, think of this model as the "parent" place where the button comes from
		Button.__init__(self, label, rect, callback, model) 
		self.image = pygame.image.load(im)	#if you're passing in a COLOR instead of an image change to: self.image.fill(im)
	def clicked(self, button_name):
		self.model.currentscreen = self.model.buildscreen 	# this is where the magic happens.  Because we've declared a model
															# we can access that model (in this case, a Game, which has a currentscreen)
															# to whatever other screen we want within that model
															# currently, in RoboGame, I want the build screen to be the current screen it starts
															"""THIS IS WHAT YOU HAVE TO CHANGE"""
															# obviously, your game won't have a buildscreen, so this will throw an error
															# just change buildscreen to whatever of your screens you want your game to start
															# at after the title screen

"""
However, that's kind of an unusual example, because the button's model is the Game.  Usually, a button will be declared within a Screen
and that will change things slightly.
This clicked method is from within my buildscreen class, in the StoreButton, which is the button that lets you go from the build screen
to the store screen
"""

    def clicked(self, button_name):
        self.model.game.currentscreen = self.model.game.storescreen

# what's going on here, is that remember, the button's model is the "parent" it gets declared in, which here is the Store Screen
# so if we did the same thing as above, self.model.currentscreen, we would get an error because a StoreScreen or any other screen
# doesn't have a currentscreen
# so this is why we passed a game into each of our screens.  So they screen knows what game it came from, so that the buttons can
# set their model's game's currentscreen to the appropriate screen
# basically, in THIS example, model = Store Screen (or whatever screen), game = RoboGame (or whatever game your screen is in)

"""
One more quick type of button clicks! These are from the ModSimButton classes in the Screen Switcher
"""

	def clicked(self, button_name):
		self.model.currentGame = self.model.modsimgame
		self.model.inGame = True

# here, the model "parent" IS in fact the Model in ScreenSwitcher, because that's where they're declared
# so these buttons don't change the model's screen, they change the game the model is in
# then, because the inGame is now true, it runs the code we looked at above in the loop, the one that sets
# the Model's current screen to the game's current screen.  Such that we get game screens!