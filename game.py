import pygame
import random
import time
import gameworld
import controller

if __name__ == "__main__":
    world = gameworld.Init_World() # initalize the world
    controller = controller.Arrow_Keys_Controller()
    clock = pygame.time     .Clock() # initialize the clock
    running = True
    while running:
        clock.tick(8)
        update = gameworld.Update(world)
        for event in pygame.event.get():
            if event.type is pygame.QUIT: # if the program is closed
                running = False
            elif event.type == pygame.KEYDOWN: # if a key is pressed
                controller.pressed(event.key)
            elif event.type == pygame.KEYUP: # if a key is released
                controller.released(event.key)
        update._redraw()
        try: # finds the direction that is currently true
            dir = list(controller.direction.keys())[list(controller.direction.values()).index(True)]
            world.player.move(dir)
        except ValueError: # if True is not in the list
            pass
        try: # finds the action that is currently true
            act = list(controller.action.keys())[list(controller.action.values()).index(True)]
            # world.player.action(act)
            world.player.action(act)
        except ValueError: # if True is not in the list
            pass




    # import doctest
    # doctest.run_docstring_examples(World._door_location, globals())
