import pygame
import gameworld
from pygame import transform
import time
import random
from game import Game

def angle_to_dir(angle):
    """Converts an angle to left, right, up, or down

    opposite: get the opposite of the given angle"""
    if angle == 0:
        return 'up'
    elif angle == 90:
        return 'left'
    elif angle == 180:
        return 'down'
    elif angle == 270:
        return  'right'

def get_rev_dir(direction):
    """Get the opposite direction"""
    if direction == 'up':
        return 'down'
    elif direction == 'left':
        return 'right'
    elif direction == 'down':
        return 'up'
    elif direction == 'right':
        return 'left'

class Cell():
    def __init__(self, draw_screen, coordinates, dimensions):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.dimensions = dimensions

    def draw(self):
        """Draws a cell onto the background"""
        self.draw_screen.blit(tuple(self.coordinates))

class Actor():
    def __init__(self, cell_coordinates, world, image_loc,
                 removable=True, deadly=False, is_obstacle=True):
        self.is_obstacle = is_obstacle # cancollide?
        self.removable = removable
        self.deadly = deadly # death on touch?
        self.world = world
        # takes coordinates as a tuple
        # if self.world._is_occupied(cell_coordinates):
        #     raise Exception('%s is already occupied!' % cell_coordinates)
        self.cell_coordinates = cell_coordinates # sets the position of the Actor
        self.facing = 0 # angle

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

    def is_valid(self, coord):
        """Checks if the space the player wants to move to can be moved to

        coord: The coordinate to check if valid"""
        return (self.world._is_in_grid(coord) # checks if in the world
                and not self.world._is_occupied(coord)) # checks if occupied

    def next_space(self, direction, distance = 1):
        """Find the next space
        direction: direction to go
        distance: how many spaces to go"""
        if direction == 'up':
            return (self.cell_coordinates[0], self.cell_coordinates[1] - 1)
        elif direction == 'left':
            return (self.cell_coordinates[0] - 1, self.cell_coordinates[1])
        elif direction == 'down':
            return (self.cell_coordinates[0], self.cell_coordinates[1] + 1)
        elif direction == 'right':
            return (self.cell_coordinates[0] + 1, self.cell_coordinates[1])
    def move(self, direction):
        """Moves an actor.

        direction: the direction to move the actor"""
        new_coord = self.cell_coordinates
        if direction == 'up':
            if self.facing == 0: # if already facing up
                new_coord = self.next_space('up')
            else: # if not facing up, rotate up
                new_image = transform.rotate(self.image_orig, 0)
                new_facing = 0
        elif direction == 'left':
            if self.facing == 90: # if already facing left
                new_coord = self.next_space('left')
            else: # if not facing left, rotate left
                new_image = transform.rotate(self.image_orig, 90)
                new_facing = 90
        elif direction == 'down':
            if self.facing == 180: # if already facing down
                new_coord = self.next_space('down')
            else: # if not facing down, rotate down
                new_image = transform.rotate(self.image_orig, 180)
                new_facing = 180
        elif direction == 'right':
            if self.facing == 270: # if already facing right
                new_coord = self.next_space('right')
            else: # if not facing right, rotate right
                new_image = transform.rotate(self.image_orig, 270)
                new_facing = 270
        if new_coord != self.cell_coordinates and self.is_valid(new_coord): # if the coord changed and is valid
                self.cell_coordinates = new_coord
        else:
            try:
                self.image = new_image
                self.facing = new_facing
            except UnboundLocalError: # if the item has not moved or rotated
                pass # ie no new image
                # return None # ie no new image

class Player(Actor):
    """Creates the Player to place on the map"""
    def __init__(self, initial_coordinates, world, image_location):
        """Initialize the Player.
        initial_coordinates: the starting coordinates for the player
        world: the map
        image_location: file path of the image for the player"""
        super(Player, self).__init__(
            initial_coordinates, world, image_location, removable=False, is_obstacle=False) # uses the __init__ method from Actor()
        self.cells = world.cells
        self.image_orig = self.image # an original image to base off of that does not rotate

    def action(self, act):
        """Execute an action for the Player"""
        if act == 'sword':
            self.sword = Sword(self, self.world)

class Sword(Actor):
    """Sword object to attack"""

    def __init__(self, player, world, image_location = './images/sword.jpg'):
        """Initialize the sword object"""
        super(Sword, self).__init__(
            player.cell_coordinates, world, image_location, removable=True, is_obstacle=False) # uses the __init__ method from Actor()
        self.facing = player.facing
        self._get_coordinates()
        self._swing()

    def _get_coordinates(self):
        """Find the space immediately in front of the player to swing in"""
        if self.facing == 0:
            self.cell_coordinates = (self.cell_coordinates[0], self.cell_coordinates[1] - 1)
            self.image = transform.rotate(self.image_orig, 0)
        elif self.facing == 180:
            self.cell_coordinates = (self.cell_coordinates[0], self.cell_coordinates[1] + 1)
            self.image = transform.rotate(self.image_orig, 180)
        elif self.facing == 90:
            self.cell_coordinates = (self.cell_coordinates[0] - 1, self.cell_coordinates[1])
            self.image = transform.rotate(self.image_orig, 90)
        elif self.facing == 270:
            self.cell_coordinates = (self.cell_coordinates[0] + 1, self.cell_coordinates[1])
            self.image = transform.rotate(self.image_orig, 270)

    def _swing(self):
        """Check if the sword hits an npc"""
        self.world.actors_position.append(self.cell_coordinates) # add the sword
        self.world.actors.append(self)
        gameworld.Update(self.world)._redraw() # draw the sword
        time.sleep(.5) # how long to swing
        # GET THE CURRENT TICK OF THE WORLD
        # GET A VALUE OF THE TICK WHERE IT SHOULD GO AWAY
        # HAVE THE UPDATE CLASS DEAL WITH REMOVING THE SWORD
        self.world.actors_position.remove(self.cell_coordinates) # remove the sword
        self.world.actors.remove(self)

        pos = self.world.actors_position.index(self.cell_coordinates) # get the position of the coord in the list
        actor = self.world.actors[pos] # get the actor that is at that coord
        if actor.removable == True:
            actor.health += -1 # remove one health, only exists if the item is removable
            if actor.health <= 0: # if dead
                del self.world.actors_position[pos] # get rid of the swing from the list of actors
                del self.world.actors[pos]

class Npc(Actor):
    """Creates an NPC to place in the world"""
    def __init__(self, initial_coordinates, world, image_location, health = 2):
        """Initialize the NPC.
        initial_coordinates: the starting coordinates for the NPC
        world: the map
        image_location: file path of the image for the NPC
        health = number of hits until dead"""
        super(Npc, self).__init__(
            initial_coordinates, world, image_location, removable=True, deadly=True, is_obstacle=True) # uses the __init__ method from Player()
        self.health = health

class Grunt(Npc):
    """Basic NPC that walks back and forth until it hits an obstacle,
    then it turns around and walks back to its starting position."""
    def __init__(self, initial_coordinates, world, image_location, health = 1, move_angle = random.randint(0, 3) * 90):
        """Initialize the Grunt.
        initial_coordinates: starting position for the Grunt
        world: the map
        image_location: file path of the image for the NPC
        health = number of hits until dead
        mov_dir = the direction the npc moves in"""
        super(Grunt, self).__init__(
        initial_coordinates, world, image_location, health)
        self.move_dir = angle_to_dir(move_angle)

    def action(self):
        """Move the Grunt in the correct direction and at the correct space"""
        old_coord = self.cell_coordinates
        self.move(self.move_dir)
        if self.world._is_occupied(self.next_space(self.move_dir)) : # if the npc will hit the room
            self.move_dir = get_rev_dir(self.move_dir)
        # when turning around, stab?

class Hill(Actor):
    """Creates a hill to place in the world"""
    def __init__(self, initial_coordinates, world, image_location):
        """Initialize the Hill.
        initial_coordinates: the starting coordinates for the Hill
        world: the map
        image_location: file path of the image for the hill"""
        super(Hill, self).__init__(
            initial_coordinates, world, image_location, removable=False)

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
