#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from world import *

# Import components and system
from components import *
from system import *


FPS = 60
RESOLUTION = 45, 30
TILES_WIDTH = 16

################################
#  The main core of the program:
################################


def run():
    # Initialize Pygame stuff
    pygame.init()
    window = pygame.display.set_mode((RESOLUTION[0]*TILES_WIDTH, RESOLUTION[1]*TILES_WIDTH))
    pygame.display.set_caption("RPG ECS")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    # Initialize world
    world = World()

    # Create a "player" Entity with a few Components.
    player = world.create_entity()
    world.add_component(player, Position(x=0, y=0))
    world.add_component(player, Velocity(x=0, y=0))
    world.add_component(player, Renderable(image=pygame.image.load("redsquare.png")))

    # Create an ennemy Entity with a few Components.
    ennemy = world.create_entity()
    world.add_component(ennemy, Position(x=20, y=0))
    world.add_component(ennemy, Velocity(x=0, y=0))
    world.add_component(ennemy, Collideable())
    world.add_component(ennemy, Renderable(image=pygame.image.load("redsquare.png")))

    # Create some Processor instances, and asign them to be processed.
    render_processor = RenderProcessor(window=window, minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1], tiles_width=TILES_WIDTH)
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
                    if world.component_for_entity(player, Position).y == 0:
                        print("Youhou!! That's a jump!")
                        world.component_for_entity(player, Velocity).y = 4
                    else:
                        print("You're not on the floor")
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    world.component_for_entity(player, Velocity).x = 0

        # A single call to world.process() will update all Processors:
        world.process()

        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()
