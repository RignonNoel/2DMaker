import os

PROJECT_NAME = "My first game"
FPS = 60
RESOLUTION = 45, 30
TILES_WIDTH = 16

TILES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/tiles/')
MAPS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/maps/')
OBJECT_TYPES_XML = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/config/objecttypes.xml')