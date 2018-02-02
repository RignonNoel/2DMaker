import pygame

from ECS.world import *
from components.components import *
from tiles.Tileset import *


class RenderProcessor(Processor):
    def __init__(self, window, min_x, max_x, min_y, max_y,
                 clear_color=(0, 0, 0), tiles_size=16):

        super().__init__()
        self.window = window
        self.clear_color = clear_color
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.margin = 0
        self.tiles_size = tiles_size

    def process(self):
        # Clear the window:
        self.window.fill(self.clear_color)

        # This will iterate over every Entity
        # that has this Component, and blit it:
        list_entities = self.world.get_components(Position, Renderable)
        for ent, (position, renderable) in list_entities:
            if self.world.has_component(ent, Direction):
                direction = self.world.component_for_entity(ent, Direction)
                if direction.direction == 'LEFT':
                    self.display_image(
                        renderable.image_left,
                        position.x,
                        position.y
                    )
                if direction.direction == 'RIGHT':
                    self.display_image(
                        renderable.image_right,
                        position.x,
                        position.y
                    )
                if direction.direction == 'TOP':
                    self.display_image(
                        renderable.image_top,
                        position.x,
                        position.y
                    )
                if direction.direction == 'BOTTOM':
                    self.display_image(
                        renderable.image_bottom,
                        position.x,
                        position.y
                    )
            else:
                # We display a default image
                # if we have no direction
                self.display_image(
                    renderable.image_bottom,
                    position.x,
                    position.y
                )

        # Flip the framebuffers
        pygame.display.flip()

    def display_image(self, image, position_x, position_y):
        self.window.blit(
            image,
            (
                position_x*self.tiles_size,
                (self.max_y-position_y-1)*self.tiles_size
            )
        )

    def display_tiles(self, tile_x, tile_y, position_x,
                      position_y, tile_manager):

        self.window.blit(
            tile_manager.get_tile(tile_x, tile_y),
            (
                position_x*self.tiles_size,
                position_y*self.tiles_size
            )
        )
