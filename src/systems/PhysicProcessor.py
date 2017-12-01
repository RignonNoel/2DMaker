from ECS.world import *
from components.components import *
from tiles.Tileset import *


class PhysicProcessor(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def process(self):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (vel, position, direction) in self.world.get_components(Velocity, Position, Direction):
            # Update with velocity
            self.process_velocity(ent, vel, position)

            # Update direction of entities
            self.process_direction(vel, direction)

            # Keep the player in the map
            position.x = max(self.minx, position.x)
            position.y = max(self.miny, position.y)
            position.x = min(self.maxx-1, position.x)
            position.y = min(self.maxy-1, position.y)

    def process_direction(self, vel, direction):
        if vel.x > 0 and abs(vel.x) > abs(vel.y):
            direction.direction = 'RIGHT'

        if vel.x < 0 and abs(vel.x) > abs(vel.y):
            direction.direction = 'LEFT'

        if vel.y > 0 and abs(vel.y) > abs(vel.x):
            direction.direction = 'TOP'

        if vel.y < 0 and abs(vel.y) > abs(vel.x):
            direction.direction = 'BOTTOM'

    def process_velocity(self, ent, vel, position):
        # Update the Renderable Component's position by it's Velocity:
        collision_x = False
        collision_y = False

        # Entity go to the right
        if vel.x > 0:
            for x in range(1, vel.x+1):
                for entity in self.world.get_entities():
                    if entity != ent:
                        if self.world.has_component(entity, Collideable):
                            other_x = self.world.component_for_entity(entity, Position).x
                            other_y = self.world.component_for_entity(entity, Position).y

                            if other_y == position.y and other_x == position.x + x:
                                position.x = other_x - 1
                                collision_x = True

        # Entity go to the left
        if vel.x < 0:
            for x in range(vel.x, 0):
                for entity in self.world.get_entities():
                    if entity != ent:
                        if self.world.has_component(entity, Collideable):
                            other_x = self.world.component_for_entity(entity, Position).x
                            other_y = self.world.component_for_entity(entity, Position).y

                            if other_y == position.y and other_x == position.x + x:
                                position.x = other_x + 1
                                collision_x = True

        # Entity go to the top
        if vel.y > 0:
            for y in range(1, vel.y+1):
                for entity in self.world.get_entities():
                    if entity != ent:
                        if self.world.has_component(entity, Collideable):
                            other_x = self.world.component_for_entity(entity, Position).x
                            other_y = self.world.component_for_entity(entity, Position).y

                            if other_y == position.y + y and other_x == position.x:
                                position.y = other_y - 1
                                collision_y = True

        # Entity go to the bottom
        if vel.y < 0:
            for y in range(vel.y, 0):
                for entity in self.world.get_entities():
                    if entity != ent:
                        if self.world.has_component(entity, Collideable):
                            other_x = self.world.component_for_entity(entity, Position).x
                            other_y = self.world.component_for_entity(entity, Position).y

                            if other_y == position.y + y and other_x == position.x:
                                position.y = other_y + 1
                                collision_y = True

        # If no collision, we move to the new position
        if not collision_x:
            position.x += vel.x

        if not collision_y:
            position.y += vel.y