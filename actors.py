import pygame
import gameworld
from pygame import transform

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
        if self.world._is_occupied(cell_coordinates):
            raise Exception('%s is already occupied!' % cell_coordinates)
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
        if self.world._is_deadly(coord) == True:
            return error
        return (self.world._is_in_grid(coord) # checks if in the world
                and not self.world._is_occupied(coord)) # checks if occupied

    def move(self, direction):
        """Moves an actor.

        direction: the direction to move the player"""
        if direction == 'up':
            new_coord = (self.cell_coordinates[0], self.cell_coordinates[1] - 1)
            new_image = transform.rotate(self.image_orig, 0)
            new_facing = 0
        elif direction == 'down':
            new_coord = (self.cell_coordinates[0], self.cell_coordinates[1] + 1)
            new_image = transform.rotate(self.image_orig, 180)
            new_facing = 180
        elif direction == 'left':
            new_coord = (self.cell_coordinates[0] - 1, self.cell_coordinates[1])
            new_image = transform.rotate(self.image_orig, 90)
            new_facing = 90
        elif direction == 'right':
            new_coord = (self.cell_coordinates[0] + 1, self.cell_coordinates[1])
            new_image = transform.rotate(self.image_orig, 270)
            new_facing = 270
        if self.is_valid(new_coord): # check if the coord is valid
            self.cell_coordinates = new_coord
            self.image = new_image
            self.facing = new_facing

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

    def action(self, act):
        """Execute an action for the Player"""
        if act == 'sword':
            self.sword = Sword(self, self.world)


class Sword():
    """Sword object to attack"""

    def __init__(self, player, world):
        """Initialize the sword object"""
        self.player = player
        self.world = world
        self._get_initial_coordinates()
        self._swing()

    def _get_initial_coordinates(self):
        """Sword attack"""
        if self.player.facing == 0:
            self.cell_coordinates = (self.player.cell_coordinates[0], self.player.cell_coordinates[1] - 1)
        elif self.player.facing == 180:
            self.cell_coordinates = (self.player.cell_coordinates[0], self.player.cell_coordinates[1] + 1)
        elif self.player.facing == 90:
            self.cell_coordinates = (self.player.cell_coordinates[0] - 1, self.player.cell_coordinates[1])
        elif self.player.facing == 270:
            self.cell_coordinates = (self.player.cell_coordinates[0] + 1, self.player.cell_coordinates[1])

    def _swing(self):
        """Check if the sword hits an npc"""
        # self.player.image_loc =
        pos = self.world.actors_position.index(self.cell_coordinates) # get the position of the coord in the list
        actor = self.world.actors[pos] # get the actor that is at that coord
        if type(actor) == Npc:
            actor.health += -1 # remove one health
            if actor.health <= 0: # if dead
                del self.world.actors_position[pos]
                del self.world.actors[pos]

class Npc(Actor):
    """Creates an NPC to place in the world"""
    def __init__(self, initial_coordinates, world, image_location, health = 2):
        """Initialize the NPC.
        initial_coordinates: the starting coordinates for the NPC
        world: the map
        image_location: file path of the image for the NPC"""
        super(Npc, self).__init__(
            initial_coordinates, world, image_location, removable=True, deadly=True, is_obstacle=False) # uses the __init__ method from Player()
        self.health = health

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