import pygame
import random
import time
import gameworld
import controller

class Game():
    """Class to manage the actor and gameworld classes"""
    def __init__(self):
        """Create the world"""
        self.world = gameworld.Init_World() # initalize the world
        self.controller = controller.Arrow_Keys_Controller()
        self.clock = pygame.time.Clock() # initialize the clock

    def check_events(self, event):
        """Check the events"""
        if event.type is pygame.QUIT: # if the program is closed
            # if game.over == False?:
                #this
            # else:
                # this and this
            self.world.running = False
        elif event.type == pygame.KEYDOWN: # if a key is pressed
            self.controller.pressed(event.key)
        elif event.type == pygame.KEYUP: # if a key is released
            self.controller.released(event.key)

    def check_actions(self):
        """Checks for movement and other actions to see which is currently true"""
        try: # finds the direction that is currently true
            dir = list(self.controller.direction.keys())[list(self.controller.direction.values()).index(True)]
            self.world.player.move(dir)
        except ValueError: # if True is not in the list
            pass

    def game_over(self):
        pass

if __name__ == "__main__":
    game = Game()
    while game.world.running:
        game.clock.tick(8)
        update = gameworld.Update(game.world)
        for event in pygame.event.get():
            game.check_events(event) # check the events
        update._redraw()
        game.check_actions()
        try: # finds the action that is currently true
            act = list(game.controller.action.keys())[list(game.controller.action.values()).index(True)]
            # world.player.action(act)
            game.world.player.action(act)
        except ValueError: # if True is not in the list
            pass




    # import doctest
    # doctest.run_docstring_examples(World._door_location, globals())
