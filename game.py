import pygame

class World():
    """Grid world that contains the player, wall, sludge, and the npcs.
    The information to make this class was heavily based on information
    learned from the ai-toolbox written by Dennis Chen."""
    def __init__(self, width=20, height = 20, cell_size=50):
        """Initialize the world.
        width: The width of the world in cells
        height: The height of the world in cells
        cell_size: The dimensions of the cell in pixels"""
        pygame.init() # initialize the pygame module
        screen_size = (height * cell_size, width * cell_size)
        self.screen = pygame.display.set_mode(screen_size)
        # set the dimensions of the world
        self.width = width
        self.height = height
        self.cell_size = cell_size

    def _draw_background(self):
        """Sets the background color"""
        COLOR = (252, 216, 169) # the beige from the legend of zelda games
        self.screen.fill(COLOR)

    def _door_location(self, door_position = 'top-center', door_width = 1):
        """Determine the opening location, the places not to place wall
        tiles as a border
        door_position: The position of the door (top, bottom, left, right; dash;
        center, left, right). Also accepts random numbers 0-
        door_width: The width of the door in cells

        returns: Tuple of the position of the opening

        The following doctest was added to test if the method returns the correct
        position for the default state.
        >>> world = World()
        >>> world._door_location()
        (10.0, 0, 1)

        The following doctest was added to check if could get the door width and
        a position for a non-default state.
        >>> world = World()
        >>> world._door_location('top-left', 2)
        (1, 0, 2)"""
        pos = {
            'top-left': (1, 0, door_width),
            'top-center':(self.width/2, 0, door_width),
            'top-right': (self.width-1, 0, door_width)
        }
        return pos.get(door_position)

    def _redraw(self):
        """Updates the world view"""
        self._draw_background()
        pygame.display.update()

    def main_loop(self):
        """Update the graphics and check for events"""
        running = True
        while running: # while running the Program
            self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT: # if the program is closed
                    running = False

if __name__ == "__main__":
    # world = World() # initalize the world
    # world.main_loop() # update graphics and check for events

    import doctest
    doctest.run_docstring_examples(World._door_location, globals())
