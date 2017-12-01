from Tileset import Tileset
import settings


class TileManager:

    def __init__(self):
        pass

    @staticmethod
    def get_player_tileset():
        return Tileset(
            spreedsheet=settings.TILES_FOLDER + '/characters.png',
            tiles_size=settings.TILES_WIDTH
        )

    @staticmethod
    def get_map_tileset():
        return Tileset(
            spreedsheet=settings.TILES_FOLDER + '/basictiles.png',
            tiles_size=settings.TILES_WIDTH
        )
