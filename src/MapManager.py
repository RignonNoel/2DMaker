import xml.etree.ElementTree
import csv
import pygame


class Map:

    map = []

    def __init__(self, file):
        self.file = file

        xml_import = xml.etree.ElementTree.parse(self.file).getroot()
        self.tile_width = int(xml_import.attrib['tilewidth'])
        self.tile_height = int(xml_import.attrib['tileheight'])
        self.width = int(xml_import.attrib['width'])
        self.height = int(xml_import.attrib['height'])
        self.version = xml_import.attrib['version']
        self.orientation = xml_import.attrib['orientation']
        self.renderorder = xml_import.attrib['renderorder']
        self.nextobjectid = int(xml_import.attrib['nextobjectid'])

        # Init tilesets
        self.tilesets = []
        for tileset in xml_import.findall('tileset'):
            new_tileset = Tileset(tileset)
            self.tilesets.append(new_tileset)

        # Init layers
        self.layers = []
        for layer in xml_import.findall('layer'):
            new_layer = Layer(layer)
            self.layers.append(new_layer)


class Tileset:

    def __init__(self, tileset):
        self.firstgid = tileset.attrib['firstgid']
        self.name = tileset.attrib['name']
        self.tilewidth = tileset.attrib['tilewidth']
        self.tileheight = tileset.attrib['tileheight']
        self.tilecount = tileset.attrib['tilecount']
        self.columns = tileset.attrib['columns']

        # Init images
        self.images = []
        for image in tileset.findall('image'):
            new_image = Image(image)
            self.images.append(new_image)


class Image:

    def __init__(self, image):
        self.source = image.attrib['source']
        self.trans = image.attrib['trans']
        self.width = image.attrib['width']
        self.height = image.attrib['height']
        self.image = pygame.image.load(self.source)


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
