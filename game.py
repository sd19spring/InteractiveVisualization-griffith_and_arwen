import pygame
import random

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
        self.actors = {} # initialize the actors
        # set the dimensions of the world
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self._init_cells() # creates the cells

    def _draw_background(self):
        """Sets the background color"""
        COLOR = (252, 216, 169) # the beige from the legend of zelda games
        self.screen.fill(COLOR)

    def _init_cells(self):
        """Creates all of the cells, getting positions for each cell"""
        self.cells = {}
        cell_size = (self.cell_size, self.cell_size)
        for i in range(self.height): # go through all rows
            for j in range(self.width): # go through all columns in the row
                cell_coord = (i * self.cell_size, j * self.cell_size) # get the coordinate of that cell
                self.cells[(i, j)] = Cell(self.screen, cell_coord, cell_size) # create the cell and add it to the list

    def _add_coords(self, a, b):
        """Rewrites the current location to the place it needs to go.

        a: current position of the item
        b: the position the item is going to

        zip rewrites each element in a and b as pairs based on index:
        ((a[0], b[0]), (a[1], b[1]))
        Then, we take the sum of each of those pairs, and rewrite it as a tuple:
        (a[0]+b[0], a[1]+b[1])
        """
        return tuple(map(sum, zip(a, b)))

    def _door_location(self, door_position = random.randint(1, 4)):
        """Determine the opening location, the places not to place wall
        tiles as a border
        door_position: The position of the door based on a number. 1:top,
        2:bottom, 3: left, 4:right

        returns: Tuple of the position of the opening

        The following doctest was added to test all four positions
        >>> world = World()
        >>> world._door_location(1)
        (10, 0)
        >>> world._door_location(2)
        (10, 19)
        >>> world._door_location(3)
        (0, 10)
        >>> world._door_location(4)
        (19, 10)"""
        pos = {
            1:(int(self.width/2), 0), # center top door
            2:(int(self.width/2), self.height-1), # center bottom door
            3:(0, int(self.height/2)), # center left door
            4:(self.width-1, int(self.height/2)), # center
        }
        return pos.get(door_position)

    def _draw_doors(self):
        """Draws the doors"""
        door = Actor(self._door_location(), self, './images/door.jpg')
        door.draw()

    def _is_occupied(self, cell_coord):
        """Checks if a space is occupied by a tile."""
        try:
            actor = self.actors[cell_coord] # creates a new tile
            return actor.is_obstacle # if obscalcle, true, else False
        except KeyError: # if no keys
             return False

    def _redraw(self):
        """Updates the world view"""
        self._draw_background()
        self._draw_doors()
        pygame.display.update()

    def main_loop(self):
        """Update the graphics and check for events"""
        running = True
        while running: # while running the Program
            self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT: # if the program is closed
                    running = False

class Actor(object):
    def __init__(self, cell_coordinates, world, image_loc,
                 removable=True, is_obstacle=True):
        self.is_obstacle = is_obstacle
        self.removable = removable
        # takes coordinates as a tuple
        if world._is_occupied(cell_coordinates):
            raise Exception('%s is already occupied!' % cell_coordinates)
        self.cell_coordinates = cell_coordinates
        self.world = world
        self.image = pygame.image.load(image_loc)
        self.image_rect = self.image.get_rect()

    def draw(self):
        cells = self.world.cells
        cell = cells[self.cell_coordinates]
        # add an offset so that the image will fit inside the cell border
        x_y_coords = self.world._add_coords(cell.coordinates, (3, 3))
        rect_dim = (self.image_rect.width, self.image_rect.height)
        self.image_rect = pygame.Rect(x_y_coords, rect_dim)
        screen = self.world.screen
        screen.blit(self.image, self.image_rect)

class Tile(Actor):
    def __init__(self, cell_coordinates, world, image_location,
                 movement_cost=0, is_unpassable=True):
        super(ObstacleTile, self).__init__(
            cell_coordinates, world, image_location, removable=True,
            is_obstacle=is_unpassable)
        self.terrain_cost = terrain_cost

class Cell():
    def __init__(self, draw_screen, coordinates, dimensions):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.dimensions = dimensions

    def draw(self):
        """Draws a cell onto the background"""
        self.draw_screen.blit(self.coordinates)


if __name__ == "__main__":
    world = World() # initalize the world
    world.main_loop() # update graphics and check for events

    # import doctest
    # doctest.run_docstring_examples(World._door_location, globals())
