##################################
#  Define some Components:
##################################


class Velocity:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Collideable:
    def __init__(self, block=True):
        self.block = block


class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Renderable:
    def __init__(self, image, depth=0):
        self.image = image
        self.depth = depth
        self.w = image.get_width()
        self.h = image.get_height()