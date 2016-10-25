#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pygame
from world import *
from TilesManager import *
from MapManager import *

# Import components and system
from components import *
from system import *

FPS = 60
RESOLUTION = 45, 30
TILES_WIDTH = 16

TILES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tiles/')
MAPS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps/')

################################
#  The main core of the program:
################################


def run():
    # Initialize Pygame stuff
    pygame.init()
    window = pygame.display.set_mode((RESOLUTION[0]*TILES_WIDTH, RESOLUTION[1]*TILES_WIDTH))
    pygame.display.set_caption("RPG ECS [" + str(RESOLUTION[0]*TILES_WIDTH) + "x" + str(RESOLUTION[1]*TILES_WIDTH) + "]")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    # Initialize world
    world = World()

    # Load the map
    map = Map(MAPS_FOLDER+'/test.tmx', world)

    # Initialize tile manager
    tiles_player = TilesManager(spreedsheet=TILES_FOLDER+'/characters.png', tiles_size=TILES_WIDTH)
    tiles_map = TilesManager(spreedsheet=TILES_FOLDER+'/basictiles.png', tiles_size=TILES_WIDTH)

    # Init the map as an entity
    map_entity = world.create_entity()
    world.add_component(map_entity, Position(x=0, y=RESOLUTION[1]-1))
    world.add_component(map_entity, Renderable(pygame.image.fromstring(map.render.tobytes(), map.render.size, map.render.mode), depth=-1))

    # Create a "player" Entity with a few Components.
    player = world.create_entity()
    world.add_component(player, Direction())
    world.add_component(player, Position(x=0, y=0))
    world.add_component(player, Velocity(x=0, y=0))
    world.add_component(player, Collideable())
    world.add_component(player, Renderable(
        image_bottom=tiles_player.get_tile(4, 0),
        image_left=tiles_player.get_tile(4, 1),
        image_right=tiles_player.get_tile(4, 2),
        image_top=tiles_player.get_tile(4, 3)
    ))

    # Blocs of test for collision
    bloc = world.create_entity()
    world.add_component(bloc, Position(x=20, y=3))
    world.add_component(bloc, Collideable())
    world.add_component(bloc, Renderable(tiles_map.get_tile(2, 0)))

    bloc = world.create_entity()
    world.add_component(bloc, Position(x=21, y=3))
    world.add_component(bloc, Collideable())
    world.add_component(bloc, Renderable(tiles_map.get_tile(2, 0)))

    # Create some Processor instances, and asign them to be processed.
    render_processor = RenderProcessor(window=window, minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1], tiles_width=TILES_WIDTH, tiles_player=tiles_player)
    physic_processor = PhysicProcessor(minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])
    world.add_processor(render_processor)
    world.add_processor(physic_processor)

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
                    world.component_for_entity(player, Velocity).x = -1
                elif event.key == pygame.K_RIGHT:
                    # For clarity, here is an alternate way in which a
                    # temporary variable is created and modified. The previous
                    # way above is recommended instead.
                    player_velocity_component = world.component_for_entity(player, Velocity)
                    player_velocity_component.x = 1
                elif event.key == pygame.K_UP:
                    world.component_for_entity(player, Velocity).y = 1
                elif event.key == pygame.K_DOWN:
                    world.component_for_entity(player, Velocity).y = -1
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    world.component_for_entity(player, Velocity).x = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    world.component_for_entity(player, Velocity).y = 0

        # A single call to world.process() will update all Processors:
        world.process()

        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()
