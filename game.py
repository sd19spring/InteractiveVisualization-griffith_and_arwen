import pygame
import random
import time
import gameworld
import controller

class Game():
    """Class to manage the actor and gameworld classes"""
    def __init__(self):
        self.world = gameworld.Init_World() # initalize the world
        self.controller = controller.Arrow_Keys_Controller()
        self.clock = pygame.time.Clock() # initialize the clock
if __name__ == "__main__":
    game = Game()
    # world = gameworld.Init_World() # initalize the world
    # controller = controller.Arrow_Keys_Controller()
    # clock = pygame.time.Clock() # initialize the clock
    while game.world.running:
        game.clock.tick(8)
        update = gameworld.Update(game.world)
        for event in pygame.event.get():
            if event.type is pygame.QUIT: # if the program is closed
                game.world.running = False
            elif event.type == pygame.KEYDOWN: # if a key is pressed
                game.controller.pressed(event.key)
            elif event.type == pygame.KEYUP: # if a key is released
                game.controller.released(event.key)
        update._redraw()
        try: # finds the direction that is currently true
            dir = list(game.controller.direction.keys())[list(game.controller.direction.values()).index(True)]
            game.world.player.move(dir)
        except ValueError: # if True is not in the list
            pass
        try: # finds the action that is currently true
            act = list(game.controller.action.keys())[list(game.controller.action.values()).index(True)]
            # world.player.action(act)
            game.world.player.action(act)
        except ValueError: # if True is not in the list
            pass




    # import doctest
    # doctest.run_docstring_examples(World._door_location, globals())
