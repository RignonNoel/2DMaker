from world import *
import pygame
from components import *

################################
#  Define some Processors:
################################
class PhysicProcessor(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def process(self):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (vel, position) in self.world.get_components(Velocity, Position):
            # Lost of velocity from gravity
            vel.y -= 1

            # Update the Renderable Component's position by it's Velocity:
            for entity in self.world.get_entities():
                if entity != ent:
                    other_x = self.world.component_for_entity(entity, Position).x
                    other_y = self.world.component_for_entity(entity, Position).y

                    # Entity go to the right
                    if vel.x >= 0:
                        if other_y == position.y and other_x in range(position.x, position.x+vel.x + 1):
                            print('Seems you have a collision!')
                            position.x = other_x - 1
                        else:
                            position.x += vel.x

                    # Entity go to the right
                    if vel.x < 0:
                        if other_y == position.y and other_x in range(position.x + vel.x, position.x + 1):
                            print('Seems you have a collision!')
                            position.x = other_x + 1
                        else:
                            position.x += vel.x

                    # Entity go to the top
                    if vel.y >= 0:
                        if other_x == position.x and other_y in range(position.y, position.y + vel.y + 1):
                            print('Ouch! Your head in the top!')
                            position.y = other_y - 1
                        else:
                            position.y += vel.y

                    # Entity go to the bottom
                    if vel.y < 0:
                        if other_x == position.x and other_y in range(position.y + vel.y, position.y + 1):
                            print("Oh! It's a step!!")
                            position.y = other_y + 1
                        else:
                            position.y += vel.y
            # An example of keeping the sprite inside screen boundaries. Basically,
            # adjust the position back inside screen boundaries if it tries to go outside:
            position.x = max(self.minx, position.x)
            position.y = max(self.miny, position.y)
            position.x = min(self.maxx, position.x)
            position.y = min(self.maxy, position.y)


class RenderProcessor(Processor):
    def __init__(self, window, minx, maxx, miny, maxy, clear_color=(0, 0, 0), tiles_width=16):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

        self.tiles_width = tiles_width

    def process(self):
        # Clear the window:
        self.window.fill(self.clear_color)

        # This will iterate over every Entity that has this Component, and blit it:
        for ent, (position, renderable) in self.world.get_components(Position, Renderable):
            self.window.blit(renderable.image, (position.x*self.tiles_width, (self.maxy-position.y-1)*self.tiles_width))
        # Flip the framebuffers
        pygame.display.flip()
