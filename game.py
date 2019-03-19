import pygame
from pygame import transform
import random
import time

class Init_World():
    """Initialize the world"""
    def __init__(self, width=15, height = 15, cell_size=45):
        """Initialize the world.
        width: The width of the world in cells
        height: The height of the world in cells
        cell_size: The dimensions of the cell in pixels"""
        pygame.init() # initialize the pygame module
        screen_size = (height * cell_size, width * cell_size)
        self.screen = pygame.display.set_mode(screen_size)
        # self.actors = {} # initialize the actors
        self.actors = []
        self.actors_position = []
        # set the dimensions of the world
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self._init_cells() # creates the cells
        self._init_door()
        self._init_border()
        self._init_player()
        self._init_npcs()

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

    def _is_occupied(self, cell_coord):
        """Checks if a space is occupied by a tile."""
        try:
            pos = self.actors_position.index(cell_coord) # get the position of the coord in the list
            actor = self.actors[pos] # get the actor that is at that coord
            return actor.is_obstacle # if obstacle, true, else False
        except ValueError: # if the actor does not exist
            return False

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

    def _init_door(self):
        """Initialize the door and add to actors"""
        self.door = Actor(self._door_location(), self, './images/door.jpg') # create the door object
        # self.actors[tuple(self.door.cell_coordinates)] = self.door # add the player to the actors list in World()
        self.actors.append(self.door)
        self.actors_position.append(self.door.cell_coordinates)

    def _init_border(self):
        """Initialize the border and add to actors. Assumes the world is square"""
        for x in range(self.width): # go through the width of the border spaces
            for y in range(0, self.height, self.height-1): # go through the top and bottom
                try:
                    self.border = Actor((x, y), self, './images/wall.jpg') # go horizontally
                    # self.actors[tuple(self.border.cell_coordinates)] = self.border
                    self.actors.append(self.border)
                    self.actors_position.append(self.border.cell_coordinates)
                except TypeError: # if the space is already occupied
                    pass
                try:
                    self.border = Actor((y, x), self, './images/wall.jpg') # go vertically
                    # self.actors[tuple(self.border.cell_coordinates)] = self.border
                    self.actors.append(self.border)
                    self.actors_position.append(self.border.cell_coordinates)
                except TypeError: # if the space is already occupied
                    pass

    def _init_hills(self, hill_count = random.randint(2, 5)):
        """Initialize the pieces in the middle of the arena"""
        # Should make hill strings
        # Need to avoid trapping player in?
            # Around the player
            # Trapping map
            # Door
        for i in range(hill_count):
            pass
        pass

    def _init_player(self):
        """Initialize the player in a random spot on the map"""
        self.player = Player((int(self.height/2), int(self.width/2)), self, './images/player.jpg') # create the player
        self.actors.append(self.player)
        self.actors_position.append(self.player.cell_coordinates)
        # need to randomize location, but consider not spawning in impassible objects

    def _init_npcs(self):
        """Initialize the npcs on the map"""
        self.npc = Npc((2, 2), self, './images/npc1.jpg')
        self.actors.append(self.npc)
        self.actors_position.append(self.npc.cell_coordinates)

    def _is_in_grid(self, cell_coord):
        """Tells whether cell_coord is valid and in range of the actual grid dimensions."""
        valid_x = 0 <= cell_coord[0] < self.width
        valid_y = 0 <= cell_coord[1] < self.height
        return valid_x and valid_y

class Update():
    """Class to update the world for each frame"""
    def __init__(self, world):
        """"""
        self.world = world
        self.actors = world.actors
        self.actors_position = world.actors_position
        self.screen = world.screen

    def _draw_background(self):
        """Sets the background color"""
        COLOR = (252, 216, 169) # the beige from the legend of zelda games
        self.screen.fill(COLOR)

    def _draw_actors(self):
        """Draws the actors"""
        # all_actors = self.actors.values() # gets the actor list from the actors dictionary in the World object
        all_actors = self.actors
        for actor in all_actors: # itterate through each actor
            # Just update the npcs and actors position
            if type(actor) == Player:
                pos = self.actors.index(actor) # get the position of the coord in the list
                if self.actors_position[pos] != actor.cell_coordinates: # if the position is not updated
                    self.actors_position[pos] = actor.cell_coordinates # update the position
            actor.draw() # draw each actor

    def _is_occupied(self, cell_coord):
        """Checks if a space is occupied by a tile."""
        try:
            pos = self.actors_position.index(cell_coord) # get the position of the coord in the list
            actor = self.actors[pos] # get the actor that is at that coord
            return actor.is_obstacle # if obstacle, true, else False
        except ValueError: # if the actor does not exist
            return False

    def _redraw(self):
        """Updates the world view"""
        self._draw_background()
        self._draw_actors()
        pygame.display.update()

    # def _is_in_grid(self, cell_coord):
    #     """Tells whether cell_coord is valid and in range of the actual grid dimensions."""
    #     valid_x = 0 <= cell_coord[0] < self.width
    #     valid_y = 0 <= cell_coord[1] < self.height
    #     return valid_x and valid_y

class Actor():

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
        self.image_orig = self.image # an original image to base off of that does not rotate
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

    def move(self, direction):
        """Moves the Player.

        direction: the direction to move the player"""
        if direction == 'up':
            new_coord = (self.cell_coordinates[0], self.cell_coordinates[1] - 1)
            new_image = transform.rotate(self.image_orig, 0)
        elif direction == 'down':
            new_coord = (self.cell_coordinates[0], self.cell_coordinates[1] + 1)
            new_image = transform.rotate(self.image_orig, 180)
        elif direction == 'left':
            new_coord = (self.cell_coordinates[0] - 1, self.cell_coordinates[1])
            new_image = transform.rotate(self.image_orig, 90)
        elif direction == 'right':
            new_coord = (self.cell_coordinates[0] + 1, self.cell_coordinates[1])
            new_image = transform.rotate(self.image_orig, 270)
        if self.is_valid(new_coord): # check if the coord is valid
            self.cell_coordinates = new_coord
            self.image = new_image

class Npc(Player):
    """Creates an NPC to place in the world"""

    def __init__(self, initial_coordinates, world, image_location):
        """Initialize the NPC.
        initial_coordinates: the starting coordinates for the NPC
        world: the map
        image_location: file path of the image for the NPC"""
        super(Npc, self).__init__(
            initial_coordinates, world, image_location) # uses the __init__ method from Player()

    def is_valid(self):
        pass

class Tile(Actor):
    """Creates a tile on to place in the world"""

    def __init__(self, cell_coordinates, world, image_location,
                 movement_cost=0, is_unpassable=True):
        """Initializes the tile.

        cell_coordinates: coordinates of the cell
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
            # also want to set the direction to up such that swinging a sword will go in the right direction
            # FUTURE
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

    # convert wasd to arrows

if __name__ == "__main__":
    world = Init_World() # initalize the world
    controller = Arrow_Keys_Controller()
    clock = pygame.time.Clock() # initialize the clock
    running = True
    while running:
        clock.tick(8)
        update = Update(world)
        for event in pygame.event.get():
            if event.type is pygame.QUIT: # if the program is closed
                running = False
            elif event.type == pygame.KEYDOWN: # if a key is pressed
                controller.pressed(event.key)
            elif event.type == pygame.KEYUP: # if a key is released
                controller.released(event.key)
        update._redraw()
        try:
            dir = list(controller.direction.keys())[list(controller.direction.values()).index(True)] # finds the direction that is currently true
            world.player.move(dir)
        except ValueError: # if True is not in the list
            pass

    # import doctest
    # doctest.run_docstring_examples(World._door_location, globals())
