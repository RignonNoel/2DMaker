from tiles.Tileset import Tileset
import settings


class TilesetManager:
    """
    Class used to manage Tileset
    """

    def __init__(self):
        pass

    @staticmethod
    def create(filename, tile_size):
        """
        Create a new Tileset instance with the filename given in argument
        :param filename: The name of the file we want to use
        :return: A Tileset instance
        """
        return Tileset(
            filename='{0}/{1}'.format(settings.TILES_FOLDER, filename),
            tiles_size=tile_size
        )

    @staticmethod
    def get_player_tileset(tile_size):
        """
        Create a new Tileset instance with the default character
        :return: A Tileset instance
        """
        return TilesetManager.create(
            filename=settings.TILES_MANAGER['DEFAULT_CHARACTER'],
            tile_size=tile_size
        )

    @staticmethod
    def get_map_tileset(tile_size):
        """
        Create a new Tileset instance with the default map
        :return: A Tileset instance
        """
        return TilesetManager.create(
            filename=settings.TILES_MANAGER['DEFAULT_MAP'],
            tile_size=tile_size
        )
