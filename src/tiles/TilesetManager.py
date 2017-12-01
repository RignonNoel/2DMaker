from tiles.Tileset import Tileset
import settings


class TilesetManager:
    """
    Class used to manage Tileset
    """

    def __init__(self):
        pass

    @staticmethod
    def create(filename):
        """
        Create a new Tileset instance with the filename given in argument
        :param filename: The name of the file we want to use
        :return: A Tileset instance
        """
        return Tileset(
            filename='{0}/{1}'.format(settings.TILES_FOLDER, filename),
            tiles_size=settings.TILES_WIDTH
        )

    @staticmethod
    def get_player_tileset():
        """
        Create a new Tileset instance with the default character
        :return: A Tileset instance
        """
        return TilesetManager.create(settings.TILES_MANAGER['DEFAULT_CHARACTER'])

    @staticmethod
    def get_map_tileset():
        """
        Create a new Tileset instance with the default map
        :return: A Tileset instance
        """
        return TilesetManager.create(settings.TILES_MANAGER['DEFAULT_MAP'])
