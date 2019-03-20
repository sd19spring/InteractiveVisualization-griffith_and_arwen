import pygame
import random
import actors

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
                self.cells[(i, j)] = actors.Cell(self.screen, cell_coord, cell_size) # create the cell and add it to the list

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
        self.door = actors.Actor(self._door_location(), self, './images/door.jpg') # create the door object
        # self.actors[tuple(self.door.cell_coordinates)] = self.door # add the player to the actors list in World()
        self.actors.append(self.door)
        self.actors_position.append(self.door.cell_coordinates)

    def _init_border(self):
        """Initialize the border and add to actors. Assumes the world is square"""
        for x in range(self.width): # go through the width of the border spaces
            for y in range(0, self.height, self.height-1): # go through the top and bottom
                try:
                    self.border = actors.Actor((x, y), self, './images/wall.jpg') # go horizontally
                    # self.actors[tuple(self.border.cell_coordinates)] = self.border
                    self.actors.append(self.border)
                    self.actors_position.append(self.border.cell_coordinates)
                except TypeError: # if the space is already occupied
                    pass
                try:
                    self.border = actors.Actor((y, x), self, './images/wall.jpg') # go vertically
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
        self.player = actors.Player((int(self.height/2), int(self.width/2)), self, './images/player.jpg') # create the player
        self.actors.append(self.player)
        self.actors_position.append(self.player.cell_coordinates)
        # need to randomize location, but consider not spawning in impassible objects

    def _init_npcs(self):
        """Initialize the npcs on the map"""
        self.npc = actors.Npc((2, 2), self, './images/npc1.jpg')
        self.actors.append(self.npc)
        self.actors_position.append(self.npc.cell_coordinates)

    def _is_in_grid(self, cell_coord):
        """Tells whether cell_coord is valid and in range of the actual grid dimensions."""
        valid_x = 0 <= cell_coord[0] < self.width
        valid_y = 0 <= cell_coord[1] < self.height
        return valid_x and valid_y

    def _is_deadly(self, cell_coord):
        """Checks if a space is deadly."""
        try:
            pos = self.actors_position.index(cell_coord) # get the position of the coord in the list
            actor = self.actors[pos] # get the actor that is at that coord
            return actor.deadly # if obstacle, true, else False
        except ValueError: # if the actor does not exist
            return False

class Update(Init_World):
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
            if type(actor) == actors.Player or type(actor) == actors.Npc:
                pos = self.actors.index(actor) # get the position of the coord in the list
                if self.actors_position[pos] != actor.cell_coordinates: # if the position is not updated
                    self.actors_position[pos] = actor.cell_coordinates # update the position
            actor.draw() # draw each actor

    def _redraw(self):
        """Updates the world view"""
        self._draw_background()
        self._draw_actors()
        pygame.display.update()