from PIL import Image


class TileSet:
    """Class used to manage tileset"""

    def __init__(self, first_gid, tile_width,
                 tile_height, columns, image_path,
                 options=None):

        self.first_gid = first_gid
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.columns = columns
        self.image_path = image_path

        if options is not None:
            self.image_trans = options.get('image_trans', None)
            self.image_width = options.get('image_width', None)
            self.image_height = options.get('image_height', None)
            self.name = options.get('name', None)
            self.tile_count = options.get('tile_count', None)
            self.margin = options.get('margin', None)

    def get_tile_by_id(self, tile_id):
        """
        Function used to get a tile by id
        :param tile_id:
        :return: An Image from PIL
        """
        # Get relative id for this tileset
        tile_id -= self.first_gid

        # Get position of the tile on the image
        columns = tile_id % self.columns
        line = tile_id // self.columns

        return self._get_tile_by_position(columns, line)

    def _get_tile_by_position(self, position_x, position_y, tile_width=1, tile_height=1):
        """
        Private function used to get a tile from the image
        :param position_x: Position x of the tile
        :param position_y: Position y of the tile
        :param tile_width: Width of the tile
        :param tile_height: Height of the tile
        :return: An Image from PIL
        """
        x_min = position_x * self.tile_width
        y_min = position_y * self.tile_height
        x_max = x_min + (tile_width * self.tile_width)
        y_max = y_min + (tile_height * self.tile_height)

        rect = (x_min, y_min, x_max, y_max)

        tile = Image.open(self.image_path).crop(rect)

        return tile
