from src.logic.misc import letter_to_color
from src.logic.misc import SNAKE_VALUES
#from src.logic.tile import BLOCK_SIZE
#import os
try:
    import pygame
except:
    pass
#import weakref
from itertools import cycle


import operator  # make SE offsetting work

aa = 30  # arrow_glyph.get_width()/2

OFFSET_PIXELS = 5  # (BLOCK_SIZE - circle_glyph.get_width()) / 2

class Move():
    def __repr__(self):
        return "(%s,%s)->(%s,%s)" % (self.x1, self.y1, self.x2, self.y2)

    def __eq__(self, other):
        return self.x1 == other.x1 and self.x2 == other.x2 and self.y1 == other.y1 and self.y2 == other.y2

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


def make_flicks():
    a = range(30,120,10)
    return a + a[::-1]

class SnakeElement():
    """ the body is comprised of these elements"""

    alpha_flicks = cycle(make_flicks())

    def __repr__(self):
        try:
            return "(%s,%s,%s,%s,%s)" % (self.snake.v, self.x, self.y, self.is_head(), self.order)
        except ReferenceError:
            return ""  # sometimes snake is weak-referenced

    def set_snake(self, snake):
        self.snake = snake
        self._flick = 0


    def process(self, animate=False):
        #if self._flick: self._flick = self._flick - 1 # decrement flicker
        if animate:
            self.alpha = SnakeElement.alpha_flicks.next()
        else:
            self.alpha = 255

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.snake = None  # must be set later!
        self.order = None  # used for initial ordering of snake.elements list
        self._flick = 0
        self.alpha = 255

    def release(self):
        self.snake = None

    def flicker(self):
        self._flick = 30

    def is_neighbour_tile(self, next_tile):
        """ disallow diagonal moves. used from Input. """
        if (next_tile.x == self.x and next_tile.y == self.y + 1 or \
           next_tile.x == self.x and next_tile.y == self.y - 1 or \
           next_tile.y == self.y and next_tile.x == self.x + 1 or \
           next_tile.y == self.y and next_tile.x == self.x - 1):
            return True
        else:
            return False

    def move(self, m):
        if m in self.get_moves():
            if self.snake.elements.index(self) == 0:
                # first in array
                tail = self.snake.elements[len(self.snake.elements)-1]
                self.snake.remove_el(tail)
                tail.x = m.x2
                tail.y = m.y2
                self.snake.elements.insert(0,tail)
            elif self.snake.elements.index(self) == len(self.snake.elements)-1:
                # last in array
                tail = self.snake.elements[0]
                self.snake.remove_el(tail)
                tail.x = m.x2
                tail.y = m.y2
                self.snake.elements.append(tail)
            self.snake.assign_to_tiles()
            return True
        else:
            return False

    def _get_neighbours(self,exclude=None):
        ns = []
        for e in self.snake.elements:
            if e.x == self.x-1 and e.y == self.y or \
                e.x == self.x and e.y == self.y-1 or \
                e.x == self.x+1 and e.y == self.y or \
                e.x == self.x and e.y == self.y+1:
                ns.append(e)
        if exclude != None:
            for e in exclude:
                if e in ns:
                    ns.remove(e)
        return ns

    def __copy__(self):
        se = SnakeElement(self.x,self.y)
        se.snake = self.snake
        return se

    def get_moves(self):
        """ returns list of valid moves for this SE """
        moves = []

        if not self.is_head(): return []

        def make_move(se,nx,ny):
            t = se.snake.map.get_tile(nx,ny)
            if t == None:
                return None
            m = None
            if t.is_walkable():
                m = Move(se.x,se.y,nx,ny)
            return m

        for x,y in [(self.x+1,self.y), (self.x-1,self.y), (self.x,self.y+1), (self.x,self.y-1)]:
            m = make_move(self,x,y)
            if m:
                moves.append(m)

        return moves

    def is_head(self):
        try:
            return (self.snake.elements.index(self) == 0) or (self.snake.elements.index(self) == len(self.snake.elements)-1)
        except ReferenceError:
            return False

    def reorder(self):
        if (len(self._get_neighbours()) >= 2):
            return
        ns = self._get_neighbours()
        excl = []
        next_el = self
        order = 1
        if order and next_el.order == None:
            self.order = 0
        while len(ns) != 0:
            excl.append(next_el)
            next_el = ns[0]
            if order and next_el.order == None:
                next_el.order = order
                order = order+1
            ns = ns[0]._get_neighbours(exclude=excl) #IGNORE:W0212

    def get_center(self):
        return self.snake.map.get_tile(self.x,self.y).get_center()

    def _get_corner(self):
        return self.snake.map.get_tile(self.x,self.y).get_corner()

    def export(self):
        return (self.x, self.y)

    def _get_neigh_rels(self,next,prev):
        foo = []
        if next and next.x == self.x - 1 or prev and prev.x == self.x - 1:
            foo.append("left")
        if next and next.y == self.y - 1 or prev and prev.y == self.y - 1:
            foo.append("top")
        if next and next.y == self.y + 1 or prev and prev.y == self.y + 1:
            foo.append("bottom")
        if next and next.x == self.x + 1 or prev and prev.x == self.x + 1:
            foo.append("right")
        return foo

    def _can_move_to(self):
        foo = []
        for m in self.get_moves():
            if m.x1 == m.x2 and m.y1+1 == m.y2: foo.append("S")
            if m.x1 == m.x2 and m.y1-1 == m.y2: foo.append("N")
            if m.x1 == m.x2+1 and m.y1 == m.y2: foo.append("W")
            if m.x1 == m.x2-1 and m.y1 == m.y2: foo.append("E")
        return foo

    def get_sprite(self,df,next,prev):
        ns = self._get_neigh_rels(next, prev)

        src = None
        deg = 0
        if len(ns) == 0:
            src = "stone"

        if len(ns) == 1:
            src = "head"
            if "left" in ns:
                deg = 180
            if "top" in ns:
                deg = 90
            if "bottom" in ns:
                deg = -90

        if "left" in ns and "right" in ns:
            src = "body"
        if "top" in ns and "bottom" in ns:
            src = "body"; deg = 90

        if "left" in ns and "bottom" in ns:
            src = "bend"

        if "left" in ns and "top" in ns:
            src = "bend"; deg = -90

        if "right" in ns and "top" in ns:
            src = "bend"; deg = 180

        if "right" in ns and "bottom" in ns:
            src = "bend"; deg = 90

        if not src:
            return
        surf = pygame.transform.rotate(SNAKE_SURFACES[src],deg)
        #if src not in ['stone']:
        surf.fill(self.snake.color,None,pygame.BLEND_RGBA_MULT)
        return surf


    def draw(self, arrows, resman=None):
        def draw_arrow(arrow,surface,offset,angle):
            ac = tuple(map(operator.add, self.get_center(), offset))
            surface.blit(pygame.transform.rotate(arrow,angle),ac)

        if not resman:
            return    
        
        sprite = resman.get_surface("stone", color=self.snake.color)

        if arrows:
            arrow = resman.get_surface("arrow", color=self.snake.color, alpha_decr=120 if self.alpha == 255 else 120+self.alpha)
        
        offset = (OFFSET_PIXELS, OFFSET_PIXELS)
        xy = self._get_corner()
        xy = tuple(map(operator.add, xy, offset))

        # if self.alpha != 255:
        #     sprite = sprite.convert_alpha()
        #     for a in xrange(sprite.get_width()):
        #         for b in xrange(sprite.get_height()):
        #             c = sprite.get_at((a,b))
        #             s = (c.r, c.g, c.b, max(0, c.a - self.alpha) if c.r or c.g or c.b else 0)
        #             sprite.set_at((a,b), s)

        self.snake.surface.blit(sprite, xy)

        if self.alpha != 255:
            halo = resman.get_surface("se_halo")#, color=self.snake.color)
            self.snake.surface.blit(halo, xy, None, pygame.BLEND_RGBA_MULT)      

        if arrows:
            ms = self._can_move_to()
            if "N" in ms: offset = (-aa,-3*aa); angle = 90; draw_arrow(arrow, self.snake.surface, offset, angle)
            if "S" in ms: offset = (-aa,aa); angle = -90; draw_arrow(arrow, self.snake.surface, offset, angle)
            if "W" in ms: offset = (-3*aa,-aa); angle = 180; draw_arrow(arrow, self.snake.surface, offset, angle)
            if "E" in ms: offset = (aa,-aa); angle = 0; draw_arrow(arrow, self.snake.surface, offset, angle)


# a snake consists of elements and a color
# it is either completed or not (on it's ziel block)
# it can be moved by it's two heads
class Snake:
    def __init__(self,mymap,v,elements,surface=None):#IGNORE:W0622
        # self.map = weakref.proxy(map)
        self.map = mymap
        self.surface = surface
        self.elements = elements
        self.v = v
        self.color = letter_to_color(v)
        if elements:
            self.assign_to_tiles()

    def release(self):
        self.map = None
        for se in self.elements:
            se.release()
        self.elements = None
    
    def set_surface(self,surface):
        self.surface = surface

    def __repr__(self):
        s = "%s:%s" % (self.v, len(self.elements)) #IGNORE:W0622
        s = s + str(self.elements)
        return s

    def remove_el(self,el):
        self.elements.remove(el)
        self.map.tiles[el.x][el.y].set_snake_el(None)

    def _get_el_at(self,a,b):
        for se in self.elements:
            if se.x == b and se.y == a:
                return se
        return None

    def assign_to_tiles(self):
        n = len(self.map.tiles[0])
        for x in xrange(n):
            for y in xrange(n):
                t = self.map.tiles[y][x]
                if t.v == 1 or t.v == '1': # no se here, move along
                    continue
                se = self._get_el_at(x,y)
                if se != None:
                    t.set_snake_el(se)

    def get_moves(self):
        ms = []
        for se in self.elements:
            ms = ms + se.get_moves()
        return ms

    @staticmethod
    def make_snakes(map,coords,surface=None):
        """ gets a coords array, which is parsed and a list of 'snake' instances is returned """
        elements = {}
        snakes = []
        n = len(coords[0])
        for x in xrange(n):
            for y in xrange(n):
                v = coords[x][y]
                set_elements = SNAKE_VALUES
                if v in set_elements:
                    if v not in elements:
                        elements[v] = []
                    se = SnakeElement(x, y)
                    elements[v].append(se)
        for v in elements:
            elms = elements[v]
            s = Snake(map,v,elms,surface=surface)
            for e in elms:
                e.set_snake(s)
            snakes.append(s)
        # reorder the elements
        for s in snakes:
            for e in s.elements:
                e.reorder() # assign them an 'order'
            s.elements = sorted(s.elements, key=lambda se: se.order) # sort by order
        del elements # is this our leak
        return snakes

    @staticmethod
    def make_elements(elems,sn):
        elements = []
        for e in elems:
            se = SnakeElement(e[0],e[1])
            se.set_snake(sn)
            elements.append(se)
        return elements

    def export(self):
        foo = {}
        foo['color'] = self.v
        foo['elements'] = []
        for e in self.elements:
            foo['elements'].append(e.export())
        return foo

    def draw(self, arrows=True, resman=None):
        clr = tuple(max(x-100,0) for x in self.color)
        clr = tuple(list(clr)+ [50])

        for i in xrange(len(self.elements)):
            se = self.elements[i]
            next = self.elements[i+1] if i < len(self.elements)-1 else None
            if next:
                pygame.draw.line(self.surface,clr, se.get_center(), next.get_center(),15)
            se.draw(arrows=arrows, resman=resman)

