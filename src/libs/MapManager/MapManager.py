from libs.Tiles.TileSet import TileSet
from .Layer import Layer

import xml.etree.ElementTree
from PIL import Image as Img


class Map:
    """Class used to manage TMX files"""

    orientation = None
    tile_sets = list()
    width = 0
    height = 0
    tile_width = 0
    tile_height = 0
    render_order = None
    next_object_id = None

    render = None
    object_types = None
    objects = None

    def __init__(self, file, config):
        """
        Constructor
        :param file: A TMX file who represent the map in XML
        :param config: An XML file who contait the config of our TMX files
        """
        self.file = file
        self.config = config

        # Parse the Tile Map XML file
        xml_content = xml.etree.ElementTree.parse(self.file).getroot()

        # Import data of the map from xml
        self.tile_width = int(xml_content.get('tilewidth'))
        self.tile_height = int(xml_content.get('tileheight'))
        self.width = int(xml_content.get('width'))
        self.height = int(xml_content.get('height'))
        self.orientation = xml_content.get('orientation')
        self.render_order = xml_content.get('renderorder')
        self.next_object_id = int(xml_content.get('nextobjectid'))

        # imports tilesets
        tilesets = xml_content.findall('tileset')
        self.tilesets = self.__import_tilesets(tilesets)

        # imports layers
        layers = xml_content.findall('layer')
        self.layers = self.__import_layers(layers)

    @staticmethod
    def __import_tilesets(tilesets_xml):
        """
        Import tilesets from the XML content
        :param tilesets_xml: A list of tilesets in XML
        :return: A list of `TileSet` object
        """
        tilesets = list()
        for tileset in tilesets_xml:
            image = tileset.find('image')

            options = dict()
            options['image_trans'] = image.get('trans')
            options['image_width'] = int(image.get('width'))
            options['image_height'] = int(image.get('height'))
            options['name'] = tileset.get('name')
            options['tile_count'] = int(tileset.get('tilecount'))
            options['margin'] = int(tileset.get('margin', 0))

            new_tileset = TileSet(
                first_gid=int(tileset.get('firstgid')),
                tile_width=int(tileset.get('tilewidth')),
                tile_height=int(tileset.get('tileheight')),
                columns=int(tileset.get('columns')),
                image_path=image.get('source'),
                options=options
            )
            tilesets.append(new_tileset)

        return tilesets

    @staticmethod
    def __import_layers(layers_xml):
        """
        Import layers from the XML content
        :param layers_xml: A list of layers in XML
        :return: A list of `Layer` object
        """
        layers = list()
        for layer in layers_xml:
            new_layer = Layer(layer)
            layers.append(new_layer)

        return layers

    def get_tile_width(self):
        return self.tile_width

    def get_tile_height(self):
        return self.tile_height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_render(self):
        """
        Return an image rendering of the map
        :return: an Image from PIL
        """
        if self.render is not None:
            return self.render
        else:
            self.__generate_render()
            return self.render

    def __generate_render(self):
        """
        Make a new image rendering of the map
        :return: an Image from PIL
        """
        # Search all used tiles to make a preload
        id_tiles_used = []
        for layer in self.layers:
            for line in layer.data:
                id_tiles_used += line

        id_tiles_used = set(id_tiles_used)

        # Preload all tiles used in the map
        tiles_render = {}
        for id_tile in id_tiles_used:
            for tileset in self.tilesets:
                list_id = range(
                    tileset.first_gid,
                    tileset.first_gid + tileset.tile_count
                )
                if id_tile in list_id:
                    tiles_render[id_tile] = tileset.get_tile_by_id(id_tile)

        # Create a new surface to add tiles inside
        render = Img.new(
            mode="RGBA",
            size=(
                self.width*self.tile_width,
                self.height*self.tile_height
            )
        )

        # For each layout of the map display all tiles
        for layer in self.layers:
            line_id = 0
            for line in layer.data:
                column_id = 0
                for elem in line:
                    if elem != 0:
                        render.paste(
                            tiles_render[elem],
                            (
                                column_id*self.tile_width,
                                line_id*self.tile_height
                            )
                        )
                    column_id += 1
                line_id += 1

        self.render = render

    def get_object_types(self):
        if self.object_types is not None:
            return self.object_types
        else:
            self.__import_object_types()
            return self.object_types

    def get_object_type(self, name):
        if self.object_types is None:
            self.__import_object_types()

        for object_type in self.object_types:
            if object_type['name'] == name:
                return object_type

        return None

    def __import_object_types(self):
        """
        Create a dictionnary with all object_types of the configuration
        :return: None
        """
        xml_content = xml.etree.ElementTree.parse(self.config).getroot()
        object_types = list()
        for object_type in xml_content.findall('objecttype'):
            new_object_type = dict()
            new_object_type['name'] = object_type.get('name')

            new_object_type['properties'] = dict()
            for property in object_type.findall('property'):
                new_property = (
                    property.get('type'),
                    property.get('default')
                )

                new_object_type['properties'][property.get('name')] \
                    = new_property

            object_types.append(new_object_type)

        self.object_types = object_types

    def get_objects(self):
        if self.objects is not None:
            return self.objects
        else:
            self.__import_objects()
            return self.objects

    def __import_objects(self):
        xml_content = xml.etree.ElementTree.parse(self.file).getroot()
        objects = list()
        for object_group in xml_content.findall('objectgroup'):
            for object in object_group.findall('object'):
                new_object = dict()
                new_object['object_type'] = object.get('type')
                new_object['gid'] = int(object.get('gid'))
                new_object['position_x'] = int(object.get('x'))

                # Mirror effect between the import and the game
                y = self.height * self.tile_height - int(object.get('y'))
                new_object['position_y'] = y

                new_object['width'] = int(object.get('width'))
                new_object['height'] = int(object.get('height'))

                objects.append(new_object)

        self.objects = objects
