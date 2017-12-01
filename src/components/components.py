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
    def __init__(self, x=0, y=0):
        if int(x) == x:
            self.x = x
        else:
            raise IOError

        if int(y) == y:
            self.y = y
        else:
            raise IOError


class Direction:
    def __init__(self, direction='BOTTOM'):
        if direction in ['RIGHT', 'LEFT', 'BOTTOM', 'TOP']:
            self.direction = direction
        else:
            raise IOError


class Renderable:
    def __init__(self, image_bottom, image_top=None, image_left=None, image_right=None, depth=0):
        self.image_bottom = image_bottom

        if image_top:
            self.image_top = image_top
        else:
            self.image_top = image_bottom

        if image_left:
            self.image_left = image_left
        else:
            self.image_left = image_bottom

        if image_right:
            self.image_right = image_right
        else:
            self.image_right = image_bottom

        self.depth = depth
        self.w = image_bottom.get_width()
        self.h = image_bottom.get_height()
