import pygame
import random
import time
import gameworld
import controller

class Game():
    """Class to manage the actor and gameworld classes"""
    def __init__(self, door_side = random.randint(0, 3) * 90, opening = None, level = 1):
        """Create the world"""
        self.door_side = door_side
        self.level = level
        self.world = gameworld.Init_World(door_side, opening, level) # initalize the world
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

    def get_complementary_opening(self):
        """Get the opening for the next room"""
        if self.door_side == 0:
            return 180
        elif self.door_side == 90:
            return 270
        elif self.door_side == 180:
            return 0
        elif self.door_side == 270:
            return 90

    def get_next_door(self):
        """Get the door for the next room"""
        open = self.get_complementary_opening()
        # find a door position that is not the opening
        door_side = open
        while door_side == open:
            door_side = random.randint(0, 3) * 90
        return door_side

class Start():
    """Start screen for the game"""
    def __init__(self):
        pygame.init()
        screen_size = (450, 450)
        self.screen = pygame.display.set_mode(screen_size)

    def _draw_background(self):
        """Sets the background color"""
        COLOR = (252, 216, 169) # the beige from the legend of zelda games
        self.screen.fill(COLOR)

    def _redraw(self):
        """Updates the world view"""
        self._draw_background()
        pygame.display.update()

def run_game(game):
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
                game = Game(game.get_next_door(), game.get_complementary_opening(), game.level + 1)
        if game.world._is_deadly(game.world.player.cell_coordinates) == True:
            game.world.running = False # close the world
        if game.world.running == False:
            print(game.level)

if __name__ == "__main__":
    start = Start()
    start_game = False
    running = True
    while running == True:
        start._redraw()
        for event in pygame.event.get():
            if event.type is pygame.QUIT: # if the program is closed
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_game = True
        if start_game == True:
            game = Game()
            run_game(game)
            start_game = False
