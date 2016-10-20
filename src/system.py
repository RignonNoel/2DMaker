from PIL import Image
import pygame

from world import *
from components import *
from TilesManager import *

################################
#  Define some Processors:
################################
class PhysicProcessor(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def process(self):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (vel, position, direction) in self.world.get_components(Velocity, Position, Direction):
            # Update with velocity
            self.process_velocity(ent, vel, position)

            # Update direction of entities
            self.process_direction(vel, direction)

            # Keep the player in the map
            position.x = max(self.minx, position.x)
            position.y = max(self.miny, position.y)
            position.x = min(self.maxx-1, position.x)
            position.y = min(self.maxy-1, position.y)

    def process_direction(self, vel, direction):
        if vel.x > 0 and abs(vel.x) > abs(vel.y):
            direction.direction = 'RIGHT'

        if vel.x < 0 and abs(vel.x) > abs(vel.y):
            direction.direction = 'LEFT'

        if vel.y > 0 and abs(vel.y) > abs(vel.x):
            direction.direction = 'TOP'

        if vel.y < 0 and abs(vel.y) > abs(vel.x):
            direction.direction = 'BOTTOM'

    def process_velocity(self, ent, vel, position):
        # Update the Renderable Component's position by it's Velocity:
        collision_x = False
        collision_y = False

        # Entity go to the right
        if vel.x > 0:
            for x in range(1, vel.x+1):
                for entity in self.world.get_entities():
                    if entity != ent:
                        if self.world.has_component(entity, Collideable):
                            other_x = self.world.component_for_entity(entity, Position).x
                            other_y = self.world.component_for_entity(entity, Position).y

                            if other_y == position.y and other_x == position.x + x:
                                position.x = other_x - 1
                                collision_x = True

        # Entity go to the left
        if vel.x < 0:
            for x in range(vel.x, 0):
                for entity in self.world.get_entities():
                    if entity != ent:
                        if self.world.has_component(entity, Collideable):
                            other_x = self.world.component_for_entity(entity, Position).x
                            other_y = self.world.component_for_entity(entity, Position).y

                            if other_y == position.y and other_x == position.x + x:
                                position.x = other_x + 1
                                collision_x = True

        # Entity go to the top
        if vel.y > 0:
            for y in range(1, vel.y+1):
                for entity in self.world.get_entities():
                    if entity != ent:
                        if self.world.has_component(entity, Collideable):
                            other_x = self.world.component_for_entity(entity, Position).x
                            other_y = self.world.component_for_entity(entity, Position).y

                            if other_y == position.y + y and other_x == position.x:
                                position.y = other_y - 1
                                collision_y = True

        # Entity go to the bottom
        if vel.y < 0:
            for y in range(vel.y, 0):
                for entity in self.world.get_entities():
                    if entity != ent:
                        if self.world.has_component(entity, Collideable):
                            other_x = self.world.component_for_entity(entity, Position).x
                            other_y = self.world.component_for_entity(entity, Position).y

                            if other_y == position.y + y and other_x == position.x:
                                position.y = other_y + 1
                                collision_y = True

        # If no collision, we move to the new position
        if not collision_x:
            position.x += vel.x

        if not collision_y:
            position.y += vel.y


class RenderProcessor(Processor):
    def __init__(self, window, minx, maxx, miny, maxy, map, tiles_map, tiles_player, clear_color=(0, 0, 0), tiles_width=16):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

        self.map = map
        self.margin = 0

        self.tiles_map = tiles_map
        self.tiles_player = tiles_player

        self.tiles_width = tiles_width

    def process(self):
        # Clear the window:
        self.window.fill(self.clear_color)

        # Display the map before each renderable entities
        self.display_map()

        # This will iterate over every Entity that has this Component, and blit it:
        for ent, (position, renderable) in self.world.get_components(Position, Renderable):
            if self.world.has_component(ent, Direction):
                direction = self.world.component_for_entity(ent, Direction)
                if direction.direction == 'LEFT':
                    self.display_image(renderable.image_left, position.x, position.y)
                if direction.direction == 'RIGHT':
                    self.display_image(renderable.image_right, position.x, position.y)
                if direction.direction == 'TOP':
                    self.display_image(renderable.image_top, position.x, position.y)
                if direction.direction == 'BOTTOM':
                    self.display_image(renderable.image_bottom, position.x, position.y)
            else:
                self.display_image(renderable.image_bottom, position.x, position.y)

        # Flip the framebuffers
        pygame.display.flip()

    def display_map(self):
        compteur_y = 0
        # Reverse the top/bottom of the map to display
        for line in self.map.map:
            compteur_x = 0
            for tile in line:
                if tile == '0':
                    self.display_tiles(0, 8, compteur_x, compteur_y, self.tiles_map)
                if tile == '1':
                    self.display_tiles(2, 1, compteur_x, compteur_y, self.tiles_map)
                if tile == '2':
                    self.display_tiles(4, 1, compteur_x, compteur_y, self.tiles_map)
                if tile == '3':
                    self.display_tiles(0, 1, compteur_x, compteur_y, self.tiles_map)
                if tile == 'e':
                    self.display_tiles(1, 7, compteur_x, compteur_y, self.tiles_map)
                compteur_x += 1
            compteur_y += 1

    def display_image(self, image, position_x, position_y):
        self.window.blit(image, (position_x*self.tiles_width, (self.maxy-position_y-1)*self.tiles_width))

    def display_tiles(self, tile_x, tile_y, position_x, position_y, tile_manager):
        self.window.blit(tile_manager.get_tile(tile_x, tile_y), (position_x*self.tiles_width, position_y*self.tiles_width))
