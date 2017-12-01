import os

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

PROJECT_NAME = "My first game"

FPS = 60
RESOLUTION = 45, 30
TILES_WIDTH = 16

TILES_FOLDER = os.path.join(BASE_FOLDER, 'static/tiles')
MAPS_FOLDER = os.path.join(BASE_FOLDER, 'static/maps')
OBJECT_TYPES_XML = os.path.join(BASE_FOLDER, 'static/config/objecttypes.xml')


TILES_MANAGER = {
    "DEFAULT_CHARACTER": "characters.png",
    "DEFAULT_MAP": "basictiles.png",
}
