from src.engine.utils import letter_to_color #IGNORE:E0611
from src.engine.utils import TARGETS
import pygame #@UnresolvedImport
import weakref

BLOCK_SIZE = 60
# terrain. walkable/unwalkable, ziele, etc.
class Tile():
    def get_debug_infos(self):
        return ["x:%s"%self.x, "y:%s"%self.y, "se:%s" % str(self.se) if self.se else "", "v:%s"%self.v]
        
    def get_snake_el(self):
        return self.se

    def set_snake_el(self,se):
        self.se = se

    def is_walkable(self):
        return not self.se and self.v != 1 and self.v != "1"

    def get_center(self):
        x = self.map.x_offset + BLOCK_SIZE * self.x + BLOCK_SIZE/2
        y = self.map.y_offset + BLOCK_SIZE * self.y + BLOCK_SIZE/2
        return (x,y)

    def get_corner(self):
        xy = self.get_center()
        return (xy[0] - BLOCK_SIZE/2,xy[1] - BLOCK_SIZE/2)

    def _is_target(self):
        return self.v in TARGETS

    def is_complete(self):
        "when it holds a SnakeElement of it's color or isn't a ziel tile"

        if not self._is_target():
            return True

        if not self.se:
            return False

        if self.v != self.se.snake.v.lower():
            return False

        return True

    def get_sev(self):
        if not self.se:
            return "-"
        return self.se.snake.v

    def __repr__(self):
        return str(self.v)

    def __init__(self, map, v, x, y, surface=None):
        self.map = weakref.proxy(map)
        self.surface = surface
        self.v = v
        self.x = x
        self.y = y
        self.se = None
        self.color = letter_to_color(str(v))

    def draw(self):
        if self.surface:
            pygame.draw.rect(self.surface, self.color,
                             (self.map.x_offset + BLOCK_SIZE * self.x,
                              self.map.y_offset + BLOCK_SIZE * self.y,
                              BLOCK_SIZE, BLOCK_SIZE))
