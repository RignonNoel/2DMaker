from ECS.world import *
from components.components import *


class PhysicProcessor(Processor):
    def __init__(self, min_x, max_x, min_y, max_y):
        super().__init__()
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def process(self):
        # This will iterate over every Entity
        # that has ALL of these components:
        list_components = self.world.get_components(
            Velocity,
            Position,
            Direction
        )
        for entity, (velocity, position, direction) in list_components:
            # Update with velocity
            self.process_velocity(entity, velocity, position)

            # Update direction of entities
            self.process_direction(velocity, direction)

            # Keep the player in the map
            position.x = max(self.min_x, position.x)
            position.y = max(self.min_y, position.y)
            position.x = min(self.max_x-1, position.x)
            position.y = min(self.max_y-1, position.y)

    def process_direction(self, velocity, direction):
        if velocity.x > 0 and abs(velocity.x) > abs(velocity.y):
            direction.direction = 'RIGHT'

        if velocity.x < 0 and abs(velocity.x) > abs(velocity.y):
            direction.direction = 'LEFT'

        if velocity.y > 0 and abs(velocity.y) > abs(velocity.x):
            direction.direction = 'TOP'

        if velocity.y < 0 and abs(velocity.y) > abs(velocity.x):
            direction.direction = 'BOTTOM'

    def process_velocity(self, entity, velocity, position):
        # Update the Renderable Component's position by it's Velocity:
        collision_x = False
        collision_y = False

        # Entity go to the right
        if velocity.x > 0:
            for x in range(1, velocity.x+1):
                for other_entity in self.world.get_entities():
                    if other_entity != entity:
                        if self.world.has_component(other_entity, Collideable):
                            other_x = self.world.component_for_entity(
                                other_entity,
                                Position
                            ).x
                            other_y = self.world.component_for_entity(
                                other_entity,
                                Position
                            ).y

                            if other_y == position.y \
                                    and other_x == position.x + x:
                                position.x = other_x - 1
                                collision_x = True

        # Entity go to the left
        if velocity.x < 0:
            for x in range(velocity.x, 0):
                for other_entity in self.world.get_entities():
                    if other_entity != entity:
                        if self.world.has_component(other_entity, Collideable):
                            other_x = self.world.component_for_entity(
                                other_entity,
                                Position
                            ).x
                            other_y = self.world.component_for_entity(
                                other_entity,
                                Position
                            ).y

                            if other_y == position.y \
                                    and other_x == position.x + x:
                                position.x = other_x + 1
                                collision_x = True

        # Entity go to the top
        if velocity.y > 0:
            for y in range(1, velocity.y+1):
                for other_entity in self.world.get_entities():
                    if other_entity != entity:
                        if self.world.has_component(other_entity, Collideable):
                            other_x = self.world.component_for_entity(
                                other_entity,
                                Position
                            ).x
                            other_y = self.world.component_for_entity(
                                other_entity,
                                Position
                            ).y

                            if other_y == position.y + y \
                                    and other_x == position.x:
                                position.y = other_y - 1
                                collision_y = True

        # Entity go to the bottom
        if velocity.y < 0:
            for y in range(velocity.y, 0):
                for other_entity in self.world.get_entities():
                    if entity != entity:
                        if self.world.has_component(other_entity, Collideable):
                            other_x = self.world.component_for_entity(
                                other_entity,
                                Position).x
                            other_y = self.world.component_for_entity(
                                other_entity,
                                Position
                            ).y

                            if other_y == position.y + y \
                                    and other_x == position.x:
                                position.y = other_y + 1
                                collision_y = True

        # If no collision, we move to the new position
        if not collision_x:
            position.x += velocity.x

        if not collision_y:
            position.y += velocity.y
