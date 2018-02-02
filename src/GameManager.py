import pygame
import os
from libs.MapManager.MapManager import Map
import threading
from DebugManager import DebugManager

# Import components and system
from systems.PhysicProcessor import PhysicProcessor
from systems.RenderProcessor import RenderProcessor

from ECS.world import World

# Import settings
import settings

from tiles.TilesetManager import TilesetManager
from components.components import *
import components.components as components


class GameManager:

    map = None
    window = None

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 1)

        # Initialize world
        self.world = World()

        # Load the map
        map_file = settings.MAPS_FOLDER + '/test.tmx'
        configuration_file = settings.OBJECT_TYPES_XML
        self.load_map(
            map_file=map_file,
            configuration_file=configuration_file
        )

        # Init a window to display interface
        self.init_window()

        # generate entities in the world
        self.load_entities()

        # Initialize tile manager
        self.tiles_player = TilesetManager.get_player_tileset(
            tile_size=self.map.get_tile_width()
        )
        self.tiles_map = TilesetManager.get_map_tileset(
            tile_size=self.map.get_tile_width()
        )

        # Init the map as an entity
        map_entity = self.world.create_entity()

        self.world.add_component(
            map_entity,
            Position(
                x=0,
                y=self.map.get_height() - 1
            )
        )

        render = self.map.get_render()

        self.world.add_component(
            map_entity,
            Renderable(
                pygame.image.fromstring(
                    render.tobytes(),
                    render.size,
                    render.mode
                ),
                depth=-1
            )
        )

        # Create a "player" Entity with a few Components.
        self.init_player()

        # Create some Processor instances
        # and assign them to be processed.
        self.launch_processors()

        # Launch a debugging console
        # in a new thread
        debug_manager = DebugManager()
        console_thread = threading.Thread(target=debug_manager.run)
        console_thread.setDaemon(True)
        console_thread.start()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.world.component_for_entity(self.player, Velocity).x = -1
                    elif event.key == pygame.K_RIGHT:
                        self.world.component_for_entity(self.player, Velocity).x = 1
                    elif event.key == pygame.K_UP:
                        self.world.component_for_entity(self.player, Velocity).y = 1
                    elif event.key == pygame.K_DOWN:
                        self.world.component_for_entity(self.player, Velocity).y = -1
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self.world.component_for_entity(self.player, Velocity).x = 0
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        self.world.component_for_entity(self.player, Velocity).y = 0

            # A single call to world.process() will update all Processors:
            self.world.process()

            self.clock.tick(settings.FPS)

    def init_window(self):
        """
        Init the window
        :return: Nothing
        """
        self.window = pygame.display.set_mode(
            (
                self.map.get_width() * self.map.get_tile_width(),
                self.map.get_height() * self.map.get_tile_height()
            )
        )

        pygame.display.set_caption(settings.PROJECT_NAME)

    def init_player(self):
        self.player = self.world.create_entity()
        self.world.add_component(self.player, Direction())
        self.world.add_component(self.player, Position(x=0, y=0))
        self.world.add_component(self.player, Velocity(x=0, y=0))
        self.world.add_component(self.player, Collideable())
        self.world.add_component(self.player, Renderable(
            image_bottom=self.tiles_player.get_tile(4, 0),
            image_left=self.tiles_player.get_tile(4, 1),
            image_right=self.tiles_player.get_tile(4, 2),
            image_top=self.tiles_player.get_tile(4, 3)
        ))

    def load_map(self, map_file, configuration_file):
        """
        Load a new map
        :param map_file: A TMX file of the map we want to load
        :param configuration_file: An XML configuration file of TMX
        :return: Nothing
        """
        self.map = Map(
            map_file,
            configuration_file
        )

    def load_entities(self):
        """
        Load entity of the current map
        :return: Nothing
        """
        for entity in self.map.get_objects():
            new_entity = self.world.create_entity()
            self.world.add_component(
                new_entity,
                Position(
                    x=entity['position_x']//self.map.get_tile_height(),
                    y=entity['position_y']//self.map.get_tile_width()
                )
            )
            if entity['object_type']:
                object_type = self.map.get_object_type(entity['object_type'])
                for property in object_type['properties'].keys():
                    component_name = property.split('/')[0]
                    attribut_name = property.split('/')[1]

                    # Get the class of component
                    method_of_component = getattr(components, component_name)

                    # Init component
                    component = method_of_component()
                    property_type = object_type['properties'][property][0]
                    if property_type == 'string':
                        default = str(object_type['properties'][property][1])
                    elif property_type == 'int':
                        default = int(object_type['properties'][property][1])
                    elif property_type == 'bool':
                        default = bool(object_type['properties'][property][1])

                    setattr(component, attribut_name, default)
                    # Add component to entity
                    self.world.add_component(new_entity, component)

    def launch_processors(self):
        """
        Launch all processors
        :return: Nothing
        """
        render_processor = RenderProcessor(
            window=self.window,
            minx=0,
            maxx=self.map.get_width(),
            miny=0,
            maxy=self.map.get_height(),
            tiles_width=self.map.get_tile_width(),
            tiles_player=self.tiles_player
        )
        self.world.add_processor(render_processor)

        physic_processor = PhysicProcessor(
            minx=0,
            maxx=self.map.get_width(),
            miny=0,
            maxy=self.map.get_height()
        )
        self.world.add_processor(physic_processor)