import xml.etree.ElementTree
import csv
from PIL import Image as Img
import re


class Map:

    map = []

    def __init__(self, file):
        self.file = file

        # Parse the Tile Map XML file
        xml_import = xml.etree.ElementTree.parse(self.file).getroot()

        # Import all data from xml
        self.tile_width = int(xml_import.attrib['tilewidth'])
        self.tile_height = int(xml_import.attrib['tileheight'])
        self.width = int(xml_import.attrib['width'])
        self.height = int(xml_import.attrib['height'])
        self.version = xml_import.attrib['version']
        self.orientation = xml_import.attrib['orientation']
        self.render_order = xml_import.attrib['renderorder']
        self.next_object_id = int(xml_import.attrib['nextobjectid'])

        # import tilesets from xml
        self.tilesets = []
        for tileset in xml_import.findall('tileset'):
            new_tileset = Tileset(tileset)
            self.tilesets.append(new_tileset)

        # import layers from xml
        self.layers = []
        for layer in xml_import.findall('layer'):
            new_layer = Layer(layer)
            self.layers.append(new_layer)

        # generate render
        self.render = self.get_render()

    def get_render(self):
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
                if id_tile in range(tileset.first_gid, tileset.first_gid + tileset.tile_count):
                    tiles_render[id_tile] = tileset.get_tile_by_id(id_tile)

        print(tiles_render)

        # Create a new surface to add tiles inside
        render = Img.new(mode="RGBA", size=(self.width*self.tile_width, self.height*self.tile_height))

        # For each depth of the map display all tile
        for layer in self.layers:
            line_id = 0
            for line in layer.data:
                column_id = 0
                for elem in line:
                    if elem != 0:
                        render.paste(tiles_render[elem], (column_id*self.tile_width, line_id*self.tile_height))
                    column_id += 1
                line_id += 1
        return render


class Tileset:

    def __init__(self, tileset):
        self.first_gid = int(tileset.attrib['firstgid'])
        self.name = tileset.attrib['name']
        self.tile_width = int(tileset.attrib['tilewidth'])
        self.tile_height = int(tileset.attrib['tileheight'])
        self.tile_count = int(tileset.attrib['tilecount'])
        self.columns = int(tileset.attrib['columns'])

        if 'margin' in tileset.attrib.keys():
            self.margin = int(tileset.attrib['margin'])
        else:
            self.margin = 0

        # Init image if exist
        for image in tileset.findall('image'):
            self.image = Image(image)

    def get_tile_by_id(self, id):
        # Rectify ID
        id -= self.first_gid

        # Get coord in tiles
        columns = id % self.columns
        line = id // self.columns

        print(id)
        # Get and return the tile
        return self.get_tile_by_position(columns, line)

    def get_tile_by_position(self, tile_x, tile_y, tile_width=1, tile_height=1):
        # Cut the tile from the source image
        x_min = tile_x*self.tile_width
        y_min = tile_y*self.tile_height
        x_max = x_min + tile_width*self.tile_width
        y_max = y_min + tile_height*self.tile_height
        rect = (x_min, y_min, x_max, y_max)
        print(rect)
        tile = self.image.image.crop(rect)
        print(tile.size)

        return tile


class Image:

    def __init__(self, image):
        self.source = re.compile("tiles/.*").findall(image.attrib['source'])[0]
        self.trans = image.attrib['trans']
        self.width = image.attrib['width']
        self.height = image.attrib['height']
        self.image = Img.open(self.source)


class Layer:

    def __init__(self, layer):
        self.name = layer.attrib['name']
        self.width = layer.attrib['width']
        self.height = layer.attrib['height']

        # Init data if exist
        for data in layer.findall('data'):
            self.encoding = data.attrib['encoding']
            if self.encoding == 'csv':
                self.data = self.get_data(data.text)

    def get_data(self, csv_text):
        data = []
        compteur = 0
        line = []
        for element in csv_text.split(','):
            compteur += 1
            line.append(int(element))

            if compteur % 45 == 0:
                data.append(line)
                line = []

        return data
