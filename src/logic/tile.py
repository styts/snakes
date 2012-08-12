from src.logic.misc import letter_to_color  # IGNORE:E0611
from src.logic.misc import TARGETS
import pygame  # @UnresolvedImport

BLOCK_SIZE = 68

#pygame.display.get_init()
# FIXME does this work on server?
shadow_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
shadow_surface.set_alpha(170)

# terrain. walkable/unwalkable, ziele, etc.
class Tile():
    def get_debug_infos(self):
        return ["x:%s"%self.x, "y:%s"%self.y, "se:%s" % str(self.se) if self.se else "", "v:%s"%self.v]
        
    def get_snake_el(self):
        return self.se

    def set_snake_el(self,se):
        self.se = se

    def is_walkable(self):
        return not self.se and (self.v != 1 and self.v != "1")

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

    def _init_helper_surface(self):
        self.helper_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.helper_surface.fill(self.color) 
        self.helper_surface.set_alpha(170)
        self.helper_surface.convert_alpha()

    def __repr__(self):
        return str(self.v)

    def __init__(self, mymap, v, x, y, surface=None):
        #self.map = weakref.proxy(map)
        self.map = mymap
        self.surface = surface
        self.v = v
        self.x = x
        self.y = y
        self.se = None
        self.color = letter_to_color(str(v))

        if self.surface: # only in graphics mode
            # we can't just fill screen, we need a helper surface if we want transparency
            self._init_helper_surface()
        else:
            self.helper_surface = None

    def release(self):
        self.map = None
        self.se = None
            
    def draw(self,debug_info=None):
        if self.surface:
            r = (self.map.x_offset + BLOCK_SIZE * self.x,
                              self.map.y_offset + BLOCK_SIZE * self.y,
                              BLOCK_SIZE, BLOCK_SIZE)

            if debug_info and debug_info.on:
                pygame.draw.rect(self.surface, self.color, r, 1) # debug border
            if self.v == 1 or self.v == '1': # don't draw unwalkable blocks - they're ugly
                return
            if not self.helper_surface:
                self._init_helper_surface()
            # blit a shadow
            ##### self.surface.blit( shadow_surface, (r[0]+5,r[1]+5) )
            self.surface.blit( self.helper_surface, r )
