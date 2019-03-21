import pygame
import random
import time
import gameworld
import controller

class Game():
    """Class to manage the actor and gameworld classes"""
    def __init__(self, door_side = random.randint(0, 3) * 90):
        """Create the world"""
        self.door_side = door_side
        self.world = gameworld.Init_World(door_side) # initalize the world
        self.controller = controller.Arrow_Keys_Controller()
        self.clock = pygame.time.Clock() # initialize the clock

    def check_events(self, event):
        """Check the events"""
        if event.type is pygame.QUIT: # if the program is closed
            self.world.running = False
        elif event.type == pygame.KEYDOWN: # if a key is pressed
            self.controller.pressed(event.key)
        elif event.type == pygame.KEYUP: # if a key is released
            self.controller.released(event.key)

    def check_direction(self):
        """Checks for an active direction"""
        try: # finds the direction that is currently true
            dir = list(self.controller.direction.keys())[list(self.controller.direction.values()).index(True)]
            self.world.player.move(dir)
        except ValueError: # if True is not in the list
            pass

    def check_actions(self):
        """Checks for an active action"""
        try: # finds the action that is currently true
            act = list(self.controller.action.keys())[list(self.controller.action.values()).index(True)]
            self.world.player.action(act)
        except ValueError: # if True is not in the list
            pass

    def get_complementary_door(self):
        """Get the door for the next room"""
        if self.door_side == 0:
            return 180
        elif self.door_side == 90:
            return 270
        elif self.door_side == 180:
            return 0
        elif self.door_side == 270:
            return 90

    def game_over(self):
        # activate your sword to play again
        pass


if __name__ == "__main__":
    game = Game()
    while game.world.running:
        game.clock.tick(8)
        update = gameworld.Update(game.world)
        for event in pygame.event.get():
            game.check_events(event) # check the events
        update._redraw()
        game.check_direction()
        game.check_actions()
        if game.world.cleared: # if the world has been cleared
            if game.world.player.cell_coordinates == game.world.door_position: # if the player is going through the door
                game = Game(game.get_complementary_door())
