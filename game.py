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
        pygame.init() # initialize pygame
        screen_size = (height * cell_size, width * cell_size)
        self.screen = pygame.display.set_mode(screen_size)
        # set the dimensions of the world
        self.width = width
        self.height = height
        self.cell_size = cell_size

    def _draw_background(self):
        """Sets the background color"""
        COLOR = (252, 216, 169)
        self.screen.fill(COLOR)

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
    world = World() # initalize the world
    world.main_loop() # update graphics and check for events
