import pygame


class TilesManager:
    def __init__(self, spreedsheet, tiles_size=16):
        self.tiles_size = tiles_size
        self.spreedsheet = pygame.image.load(spreedsheet)
        self.margin = 0

    def get_tile(self, tile_x, tile_y, tile_width=1, tile_height=1):
        rectangle = (tile_x*self.tiles_size, tile_y*self.tiles_size, tile_width*self.tiles_size, tile_height*self.tiles_size)
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.spreedsheet, (self.margin, self.margin), rect)
        return image
