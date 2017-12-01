import pygame

from ECS.world import *
from components.components import *
from tiles.Tileset import *


class RenderProcessor(Processor):
    def __init__(self, window, minx, maxx, miny, maxy, tiles_player, clear_color=(0, 0, 0), tiles_width=16):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

        self.margin = 0

        self.tiles_player = tiles_player

        self.tiles_width = tiles_width

    def process(self):
        # Clear the window:
        self.window.fill(self.clear_color)

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

    def display_image(self, image, position_x, position_y):
        self.window.blit(image, (position_x*self.tiles_width, (self.maxy-position_y-1)*self.tiles_width))

    def display_tiles(self, tile_x, tile_y, position_x, position_y, tile_manager):
        self.window.blit(tile_manager.get_tile(tile_x, tile_y), (position_x*self.tiles_width, position_y*self.tiles_width))
