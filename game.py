import pygame
import random
import time

class World():
    """Grid world that contains the player, wall, sludge, and the npcs.
    The information to make this class was heavily based on information
    learned from the ai-toolbox written by Dennis Chen."""

    def __init__(self, width=13, height = 13, cell_size=50):
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
        self._init_player()

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

    def _init_player(self):
        """Initialize the player in a random spot on the map"""
        self.player = Player([0, 0], self, './images/player.jpg') # create the player
        self.actors[0] = self.player # add the player to the actors list in World()
        # need to randomize location, but consider not spawning in impassible objects

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

    def _draw_door(self):
        """Draws the doors"""
        door = Actor(self._door_location(), self, './images/door.jpg') # create the door object
        door.draw()

    def _draw_actors(self):
        """Draws the actors"""
        all_actors = self.actors.values() # gets the actor list from the actors dictionary in the World object
        for actor in all_actors: # itterate through each actor
            # print(self.player.cell_coordinates)
            actor.draw() # draw each actor

    def _is_occupied(self, cell_coord):
        """Checks if a space is occupied by a tile."""
        try:
            actor = self.actors[tuple(cell_coord)] # creates a new tile
            return actor.is_obstacle # if obstacle, true, else False
        except KeyError: # if no keys
             return False

    def _redraw(self):
        """Updates the world view"""
        self._draw_background()
        self._draw_actors()
        self._draw_door()
        pygame.display.update()

    def _is_in_grid(self, cell_coord):
        """Tells whether cell_coord is valid and in range of the actual grid dimensions."""
        valid_x = 0 <= cell_coord[0] < self.width
        valid_y = 0 <= cell_coord[1] < self.height
        return valid_x and valid_y

    def main_loop(self):
        """Update the graphics and check for events"""
        clock = pygame.time.Clock() # initialize the clock
        pressed = {'up': False, 'down': False, 'left': False, 'right': False}
        running = True
        while running: # while running the Program
            clock.tick(6) # set the speed of the refresh rate in FPS
            self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT: # if the program is closed
                    running = False
                elif event.type == pygame.KEYDOWN: # check for key presses
                    if event.key == pygame.K_UP:
                        pressed['up'] = True
                        pressed['down'] = pressed['left'] = pressed['right'] = False
                    elif event.key == pygame.K_DOWN:
                        pressed['down'] = True
                        pressed['up'] = pressed['left'] = pressed['right'] = False
                    elif event.key == pygame.K_LEFT:
                        pressed['left'] = True
                        pressed['up'] = pressed['down'] = pressed['right'] = False
                    elif event.key == pygame.K_RIGHT:
                        pressed['right'] = True
                        pressed['up'] = pressed['down'] = pressed['left'] = False
                elif event.type == pygame.KEYUP: # check for key releases
                    if event.key == pygame.K_UP:
                        pressed['up'] = False
                    elif event.key == pygame.K_DOWN:
                        pressed['down'] = False
                    elif event.key == pygame.K_LEFT:
                        pressed['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        pressed['right'] = False
            if pressed['up']:
                self.player.move(self.player.cell_coordinates, 'Up')
            elif pressed['down']:
                self.player.move(self.player.cell_coordinates, 'Down')
            elif pressed['left']:
                self.player.move(self.player.cell_coordinates, 'Left')
            elif pressed['right']:
                self.player.move(self.player.cell_coordinates, 'Right')

            # keys = pygame.key.get_pressed()  #checking pressed keys
            # if keys[pygame.K_UP]:
            #     self.player.move(self.player.cell_coordinates, 'Up')
            # elif keys[pygame.K_DOWN]:
            #     self.player.move(self.player.cell_coordinates, 'Down')
            # elif keys[pygame.K_LEFT]:
            #     self.player.move(self.player.cell_coordinates, 'Left')
            # elif keys[pygame.K_RIGHT]:
            #     self.player.move(self.player.cell_coordinates, 'Right')
            # time.sleep(.5)

                # elif event.type is pygame.KEYDOWN: # if a key is pressed
                #     if event.key == pygame.K_UP:
                #         self.player.move(self.player.cell_coordinates, 'Up')
                #     elif event.key == pygame.K_DOWN:
                #         self.player.move(self.player.cell_coordinates, 'Down')
                #     elif event.key == pygame.K_LEFT:
                #         self.player.move(self.player.cell_coordinates, 'Left')
                #     elif event.key == pygame.K_RIGHT:
                #         self.player.move(self.player.cell_coordinates, 'Right')
class Actor(object):

    def __init__(self, cell_coordinates, world, image_loc,
                 removable=True, is_obstacle=True):
        self.is_obstacle = is_obstacle
        self.removable = removable
        # takes coordinates as a tuple
        if world._is_occupied(cell_coordinates):
            raise Exception('%s is already occupied!' % cell_coordinates)
        self.cell_coordinates = cell_coordinates # sets the position of the Actor
        self.world = world
        self.image = pygame.image.load(image_loc)
        self.image_rect = self.image.get_rect()

    def draw(self):
        cells = self.world.cells
        cell = cells[tuple(self.cell_coordinates)]
        # add an offset so that the image will fit inside the cell border
        x_y_coords = self.world._add_coords(cell.coordinates, (3, 3))
        rect_dim = (self.image_rect.width, self.image_rect.height)
        self.image_rect = pygame.Rect(x_y_coords, rect_dim)
        screen = self.world.screen
        screen.blit(self.image, self.image_rect)

class Player(Actor):
    """Creates the Player to place on the map"""

    def __init__(self, initial_coordinates, world, image_location):
        """Initialize the Player.
        initial_coordinates: the starting coordinates for the player
        world: the map
        image_location: file path of the image for the player"""
        super(Player, self).__init__(
            initial_coordinates, world, image_location, removable=False) # uses the __init__ method from Actor()
        self.cells = world.cells

    def is_valid(self, coord):
        """Checks if the space the player wants to move to can be moved to

        coord: The coordinate to check if valid"""
        return (self.world._is_in_grid(coord) # checks if in the world
                and not self.world._is_occupied(coord)) # checks if occupied

    def move(self, coord, direction):
        """Moves the Player.

        coord: the current coordinate of the player
        direction: the direction to move the player"""
        # check if coord is valid
        if direction == 'Up':
            new_coord = (self.cell_coordinates[0], self.cell_coordinates[1] - 1)
        elif direction == 'Down':
            new_coord = (self.cell_coordinates[0], self.cell_coordinates[1] + 1)
        elif direction == 'Left':
            new_coord = (self.cell_coordinates[0] - 1, self.cell_coordinates[1])
        elif direction == 'Right':
            new_coord = (self.cell_coordinates[0] + 1, self.cell_coordinates[1])
        else:
            pass
        if self.is_valid(new_coord):
            self.cell_coordinates = new_coord


class Tile(Actor):
    """Creates a tile on to place in the world"""

    def __init__(self, cell_coordinates, world, image_location,
                 movement_cost=0, is_unpassable=True):
        """Initializes the tile.

        cell_cordinates: coordinates of the cell
        world: the world object
        image_location: file path of the image for the cell
        movement_cost: cost to move through the cell
        is_unpassible: if the cell can be moved through"""
        super(ObstacleTile, self).__init__(
            cell_coordinates, world, image_location, removable=True,
            is_obstacle=is_unpassable)
        self.movement_cost = movement_cost

class Cell():
    def __init__(self, draw_screen, coordinates, dimensions):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.dimensions = dimensions

    def draw(self):
        """Draws a cell onto the background"""
        self.draw_screen.blit(tuple(self.coordinates))


if __name__ == "__main__":
    world = World() # initalize the world
    world.main_loop() # update graphics and check for events

    # import doctest
    # doctest.run_docstring_examples(World._door_location, globals())
