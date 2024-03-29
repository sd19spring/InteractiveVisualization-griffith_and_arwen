import pygame
import random
import actors
class Init_World():
    """Initialize the world"""
    def __init__(self, door_side, opening_side, level, width = 15, height = 15, cell_size=45):
        """Initialize the world.
        width: The width of the world in cells
        height: The height of the world in cells
        cell_size: The dimensions of the cell in pixels"""
        pygame.init() # initialize the pygame module
        self.door_side = door_side
        self.opening_side = opening_side
        self.level = level
        screen_size = (height * cell_size, width * cell_size)
        self.screen = pygame.display.set_mode(screen_size)
        self.actors = []
        # self.actors_position = []
        # set the dimensions of the world
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self._init_cells() # creates the cells
        self._init_door()
        self._init_opening()
        self._init_border()
        self._init_hills()
        self._init_player()
        self._init_npcs()
        self.running = True # set the program to run
        self.cleared = False # room cleared to false

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
        if cell_coord == self.opening_position:
            return True
        try:
            # fix to new method
            for actor in self.actors:
                if actor[1] == cell_coord:
                    return actor[0].is_obstacle
            # pos = self.actors_position.index(cell_coord) # get the position of the coord in the list
            # actor = self.actors[pos] # get the actor that is at that coord
            # return actor.is_obstacle # if obstacle, true, else False
        except ValueError: # if the actor does not exist
            return False

    def _get_door_location(self, door_side):
        """Determine the opening location, the places not to place wall
        tiles as a border"""
        pos = {
            0:(int(self.width/2), 0), # center top door
            90:(0, int(self.height/2)), # center left door
            180:(int(self.width/2), self.height-1), # center bottom
            270:(int(self.width-1), int(self.height/2)), # center right door
        }
        return pos.get(door_side)

    def _init_door(self):
        """Initialize the door and add to actors"""
        self.door_position = self._get_door_location(self.door_side)
        self.door = actors.Actor(self.door_position, self, './images/door.jpg') # create the door object
        self.actors.append((self.door, self.door.cell_coordinates))
        # self.actors_position.append(self.door.cell_coordinates)

    def _init_opening(self):
        """Initialize the opening"""
        if self.opening_side != None:
            self.opening_position = self._get_door_location(self.opening_side)
        else:
            self.opening_position = None

    def open_door(self):
        """Replace the door with an open door"""
        del self.actors[0]     # door is the first item added
        self.open_door = actors.Actor(self.door_position, self, './images/sludge.jpg')
        self.actors.append((self.open_door, self.open_door.cell_coordinates))
        self.space_before_opening = self.door_position

    def _init_border(self):
        """Initialize the border and add to actors. Assumes the world is square"""
        for x in range(self.width): # go through the width of the border spaces
            for y in range(0, self.height, self.height-1): # go through the top and bottom
                if not self._is_occupied((x, y)):
                    self.border = actors.Actor((x, y), self, './images/wall.jpg') # go horizontally
                    self.actors.append((self.border, self.border.cell_coordinates))
                    # self.actors_position.append(self.border.cell_coordinates)
                if not self._is_occupied((y, x)):
                    self.border = actors.Actor((y, x), self, './images/wall.jpg') # go vertically
                    self.actors.append((self.border, self.border.cell_coordinates))
                    #self.actors_position.append(self.border.cell_coordinates)

    def _init_hills(self, hill_count = random.randint(3, 6)):
        """Initialize a random number of hills in random places"""
        pos = {
            0: (2, self.height-5),
            1: (2, self.height-6),
            2: (self.width-5, 2),
            3: (3, self.height-6),
            4: (self.width-5, 3),
            5: (self.width-5, 4)
        }
        for hill in range(hill_count):
            place = random.choice(pos)
            for actor in self.actors:
                while place in actor[1]: # while the space is occupied
                    place = random.choice(pos) # generate more choices
            self.hill = actors.Hill(place, self, './images/hill.jpg')
            self.actors.append((self.hill, self.hill.cell_coordinates))
            # self.actors_position.append(self.hill.cell_coordinates)

    def _init_player(self):
        """Initialize the player at the center of the map"""
        self.player = actors.Player((int(self.height/2), int(self.width/2)), self, './images/player.jpg') # create the player
        # need to randomize location, but consider not spawning in impassible objects

    def _npc_locations(self, npc_position): #will need to change to reflect number of squares on map
        """Determines the spawn locations of NPCs in the room"""
        pos = {
            1: (2, 2),
            2: (2, self.height-3),
            3: (self.width-3, 2),
            4: (self.width-3, self.height-3),
        }
        position = pos.get(npc_position)
        while self._is_occupied(position) == True:
            position = pos.get(npc_position)
        return position

    def _init_npcs(self):
        """Initialize the npcs on the map"""
        for i in range(self.level):
            if i == 0 or i ==2: # spawn up to two npcs
                npc = actors.Npc(self._npc_locations(npc_position = random.randint(1, 4)), self, 'images/npc2.jpg')
            elif i == 1:
                # spawn lava
                pass
            elif 3 <= i >= 4: # spawn up to two ghosts
                pass
            elif i >= 5: # if on the fifth level
                pass
                # should exit the loop now
            if not self._is_occupied(npc.cell_coordinates): # if the spot is not already occupied (probably by an npc)
                self.actors.append((npc, npc.cell_coordinates))
                #self.actors_position.append(npc.cell_coordinates)

    def _is_in_grid(self, cell_coord):
        """Tells whether cell_coord is valid and in range of the actual grid dimensions."""
        valid_x = 0 <= cell_coord[0] < self.width
        valid_y = 0 <= cell_coord[1] < self.height
        return valid_x and valid_y

    def _is_deadly(self, cell_coord):
        """Checks if a space is deadly."""
        try:
            for actor in self.actors:
                if actor[1] == cell_coord:
                    return actor[0].deadly
            # pos = self.actors_position.index(cell_coord) # get the position of the coord in the list
            # actor = self.actors[pos] # get the actor that is at that coord
            # return actor.deadly # if obstacle is deadly
        except ValueError: # if the actor does not exist
            return False

class Update(Init_World):
    """Class to update the world for each frame"""
    def __init__(self, world):
        """"""
        self.world = world
        self.actors = world.actors
        # self.actors_position = world.actors_position
        self.player = world.player
        self.screen = world.screen

    def _draw_background(self):
        """Sets the background color"""
        COLOR = (252, 216, 169) # the beige from the legend of zelda games
        self.screen.fill(COLOR)

    def _npc_actions(self):
        """Execute the action of each npc"""
        for actor in self.actors: # itterate through each actor
            if type(actor[0]) == actors.Grunt:
                actor[0].action()

    # def _check_movement(self, actor):
    #     """Check if an item has moved, if it has, update the position"""
    #     pos = self.actors.index(actor) # get the position of the coord in the list
    #     if self.actors[pos] != actor.cell_coordinates: # if the position is not updated
    #         self.actors[pos] = actor.cell_coordinates # update the position

    def _draw_actors(self):
        """Draws the actors"""
        for actor in self.actors: # itterate through each actor
            #if type(actor) == actors.Npc or type(actor) == actors.Grunt:
            #    self._check_movement(actor) # check if the object has moved, if not do not update
            actor[0].draw() # draw each actor
        actor = self.player
        actor.draw()

    def _check_clear(self):
        """Checks if the world is clear of npcs"""
        if self.world.cleared == True: # if have already cleared the world
            return True
        # check if there are npcs in the world
        npc = False
        for actor in self.actors:
            if type(actor[0]) == actors.Grunt or type(actor[0]) == actors.Npc:
                npc = True
        if not npc:
            self.world.cleared = True
            self.world.open_door()

    def _redraw(self):
        """Updates the world view"""
        self._draw_background()
        self._npc_actions()
        self._draw_actors()
        self._check_clear()
        pygame.display.update()
