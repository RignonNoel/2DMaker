import pygame
import settings


class Tileset:
    """
    Library of Tile with access method in this that library
    """

    def __init__(self, filename, margin=0, tiles_size=settings.TILES_WIDTH):
        """
        Constructor
        :param filename: The filename of the tileset file
        :param tiles_size: The size of tiles contained in this tileset
        :param margin: The margin of each tile
        """

        self.tiles_size = tiles_size
        self.spreed_sheet = pygame.image.load(filename)
        self.margin = margin

    def get_tile(self, tile_x, tile_y, tile_width=1, tile_height=1):
        """
        Access to a tile of the Tileset
        :param tile_x: The position in x
        :param tile_y: The position in y
        :param tile_width: The size ratio in width
        :param tile_height: The size ration in height
        :return: An image
        """

        rectangle = (
            tile_x*self.tiles_size,
            tile_y*self.tiles_size,
            tile_width*self.tiles_size,
            tile_height*self.tiles_size
        )

        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()

        image.blit(
            self.spreed_sheet,
            (
                self.margin,
                self.margin
            ),
            rect
        )

        return image
