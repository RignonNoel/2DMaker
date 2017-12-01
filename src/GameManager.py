import pygame
from MapManager import Map
import threading
from DebugManager import DebugManager

# Import components and system
from systems.PhysicProcessor import PhysicProcessor
from systems.RenderProcessor import RenderProcessor

from world import World

# Import settings
import settings

from tiles.TilesetManager import TilesetManager
from components.components import *


class GameManager:

    def __init__(self):
        pygame.init()

        self.init_window()

        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 1)

        # Initialize world
        self.world = World()

        # Load the map
        map = Map(settings.MAPS_FOLDER + '/test.tmx', self.world)

        # Initialize tile manager
        self.tiles_player = TilesetManager.get_player_tileset()
        self.tiles_map = TilesetManager.get_map_tileset()

        # Init the map as an entity
        map_entity = self.world.create_entity()

        self.world.add_component(
            map_entity,
            Position(x=0, y=settings.RESOLUTION[1] - 1)
        )

        self.world.add_component(
            map_entity,
            Renderable(
                pygame.image.fromstring(
                    map.render.tobytes(),
                    map.render.size,
                    map.render.mode
                ),
                depth=-1
            )
        )

        # Create a "player" Entity with a few Components.
        self.init_player()

        # Blocs of test for collision
        bloc = self.world.create_entity()
        self.world.add_component(bloc, Position(x=20, y=3))
        self.world.add_component(bloc, Collideable())
        self.world.add_component(bloc, Renderable(self.tiles_map.get_tile(2, 0)))

        bloc = self.world.create_entity()
        self.world.add_component(bloc, Position(x=21, y=3))
        self.world.add_component(bloc, Collideable())
        self.world.add_component(bloc, Renderable(self.tiles_map.get_tile(2, 0)))

        # Create some Processor instances, and asign them to be processed.
        render_processor = RenderProcessor(window=self.window, minx=0, maxx=settings.RESOLUTION[0], miny=0,
                                           maxy=settings.RESOLUTION[1], tiles_width=settings.TILES_WIDTH,
                                           tiles_player=self.tiles_player)
        physic_processor = PhysicProcessor(minx=0, maxx=settings.RESOLUTION[0], miny=0, maxy=settings.RESOLUTION[1])
        self.world.add_processor(render_processor)
        self.world.add_processor(physic_processor)

        # Launch debug console in thread
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
                        # Here is a way to directly access a specific Entity's
                        # Velocity Component's attribute (y) without making a
                        # temporary variable.
                        self.world.component_for_entity(self.player, Velocity).x = -1
                    elif event.key == pygame.K_RIGHT:
                        # For clarity, here is an alternate way in which a
                        # temporary variable is created and modified. The previous
                        # way above is recommended instead.
                        player_velocity_component = self.world.component_for_entity(self.player, Velocity)
                        player_velocity_component.x = 1
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
                settings.RESOLUTION[0] * settings.TILES_WIDTH,
                settings.RESOLUTION[1] * settings.TILES_WIDTH
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
