import pygame
class Player_Controller():
    """Defines a controller that takes user input to control the Player
    object.
    """
    def __init__(self):
        """Initialize the player controller"""
        self.direction = {'up': False, 'down': False, 'left': False, 'right': False}

    def reset_direction(self):
        """Reset the pressed values"""
        self.direction = {'up': False, 'down': False, 'left': False, 'right': False}

    def set_direction (self, dir):
        """Set the direction to move in"""
        if dir == 'up':
            self.reset_direction()
            self.direction['up'] = True
        elif dir == 'down':
            self.reset_direction()
            self.direction['down'] = True
        elif dir == 'left':
            self.reset_direction()
            self.direction['left'] = True
        elif dir == 'right':
            self.reset_direction()
            self.direction['right'] = True

class Arrow_Keys_Controller(Player_Controller):
    """Defines a controller that takes input from the keyboard arrow keys.
    """
    def __init__(self):
        """Initialize the player controller"""
        super(Arrow_Keys_Controller, self).__init__() # uses the __init__ method from Controller()
        self.move_up = [pygame.K_UP, pygame.K_w, pygame.K_COMMA]
        self.move_down = [pygame.K_DOWN, pygame.K_s, pygame.K_o]
        self.move_left = [pygame.K_LEFT, pygame.K_a]
        self.move_right = [pygame.K_RIGHT, pygame.K_d, pygame.K_e]

    def pressed (self, key):
        """Check which key is pressed"""
        if key in self.move_up:
            self.set_direction('up')
        elif key in self.move_down:
            self.set_direction('down')
        elif key in self.move_left:
            self.set_direction('left')
        elif key in self.move_right:
            self.set_direction('right')

    def released (self, key):
        """Check to see if an arrow key is released"""
        if key in self.move_up:
            self.direction['up'] = False
        elif key in self.move_down:
            self.direction['down'] = False
        elif key in self.move_left:
            self.direction['left'] = False
        elif key in self.move_right:
            self.direction['right'] = False
