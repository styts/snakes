from tile import Tile
from math import floor
from tile import BLOCK_SIZE

try:
    import pygame
except:
    pass

colors = {(255,255,0,255) : 'Y',
          (255,0,0,255)   : 'R',
          (0,255,0,255) : 'G',
          (0,0,255,255) : 'B',
          (0, 0, 0, 255) : 1,
          (50, 50, 50, 255) : 1,
          (20, 20, 20, 255) : 0,
          (0, 102, 0, 255): 'g'
 }

class Map():
    def __init__(self, coordinates=None, surface=None,debug_info=None):
        self.tiles = []
        self.n = -1
        self.size_px = -1
        self.surface = None
        self.x_offset = 0#these 2 are set in app.py
        self.y_offset = 0
        if surface:
            self.surface = surface
        
        self.init(coordinates)

        self.debug_info = debug_info

    def release(self):
        for x in xrange(self.n):
            for y in xrange(self.n):
                t = self.tiles[x][y]
                t.se = None
                t.release()

            
    @staticmethod
    def _remove_all_but_one(coords):
        the_one = ()
        n = len(coords['snakes'])
        for x in xrange(n):
            for y in xrange(n):
                v = coords['snakes'][x][y]
                if v == 'G':
                    the_one = (x,y)
                    break
        for x in xrange(n):
            for y in xrange(n):
                v = coords['snakes'][x][y]
                if v in ['B','G','R','Y']:
                    if (x,y) != the_one:
                        coords['snakes'][x][y] = '0'
        return coords
    
    def get_coords(self,snakes=False):
        coords = []
        for x in xrange(self.n):
            coords.append([])
            for y in xrange(self.n):
                t = self.tiles[x][y]
                if snakes:
                    if t.se:
                        v = str(t.se.snake.v)
                    else:
                        v = "0"
                else:
                    v = t.v
                coords[x].append(v)
        return coords
    
    def __repr__(self):
        outstr = []
        for x in sorted(xrange(self.n),reverse=True):
            s = ""
            for y in xrange(self.n):
                v = self.tiles[y][x].v
                s = s + str(v)
            s = s + " "
            for y in xrange(self.n):
                sv = self.tiles[y][x].get_sev()
                s = s + str(sv)
            outstr.insert(0, s)
        return "\n".join(outstr).strip('\n')
    
    def pprint(self):
        print "== %s ==" % id(self)
        print self.__repr__()
        print "=============="
                
    def init(self,coordinates):
        self.n = len(coordinates[0])
        for x in xrange(self.n):
            self.tiles.append([])
            for y in xrange(self.n):
                v = coordinates[x][y]
                t = Tile(self, v, x, y, surface=self.surface)
                self.tiles[x].append(t)
        self.size_px = BLOCK_SIZE * self.n
        
    def set_surface(self,surface):
        for x in xrange(self.n):
            for y in xrange(self.n):
                t = self.tiles[x][y]
                t.surface = surface 
    
    def __copy__(self):
        m = Map()
        m.init(self.get_coords())
        for x in xrange(self.n):
            for y in xrange(self.n):
                t = self.tiles[x][y]
                if t.se:
                    m.tiles[x][y].se = t.se
        return m
    
    def get_tile(self,a,b):
        if a < 0 or a >= self.n or b < 0 or b >= self.n:
            return None
        t = self.tiles[a][b]
        return t 
    
    def is_complete(self):
        "a map is complete, when all end tiles are complete"
        for x in xrange(self.n):
            for y in xrange(self.n):
                t = self.tiles[x][y]
                if not t.is_complete(): return False
        return True
    
    def get_tile_at(self, x, y):
        x = x - self.x_offset
        y = y - self.y_offset
        if x > 0 and x < self.size_px and y > 0 and y < self.size_px:
            a = int(floor(x / BLOCK_SIZE))
            b = int(floor(y / BLOCK_SIZE))
            try:
                block = self.tiles[a][b]
                return block
            except IndexError:
                return None
        else:
            return None
    
    # @staticmethod 
    # we dont use images any more
    # def load_coords(map_name,just_one=False):
    #     f = os.path.join(os.getcwd(),'data','maps', '%s'%map_name)
    #     img = pygame.image.load(f)
    #     coords = {"tiles" : [], "snakes": []}
    #     # colors = {(255,255,0,255) : 'Y',
    #     #           (255,0,0,255)   : 'R',
    #     #           (0,255,0,255) : 'G',
    #     #           (0,0,255,255) : 'B',
    #     #           (0, 0, 0, 255) : 1,
    #     #           (50, 50, 50, 255) : 1,
    #     #           (20, 20, 20, 255) : 0,
    #     #           (0, 102, 0, 255): 'g'
    #     #  }
    #     w = img.get_width()
    #     h = img.get_height()
    #     for i in xrange(w):
    #         dest = 'tiles' if i<w/2 else 'snakes'
    #         shift = 0 if i<w/2 else w/2
    #         coords[dest].append([])
    #         for j in xrange(h):
    #             col = tuple(img.get_at((i,j)))
    #             v = colors[col] if col in colors else 0
    #             coords[dest][i-shift].append(v)
    #     if just_one:
    #         coords = Map._remove_all_but_one(coords)
    #     return coords

    def export(self):
        return self.get_coords()

    def draw(self):
#        if self.debug_info:
#            for i in xrange(self.mapdict.__len__()):
#                m = self.mapdict[str(i+1)]
#                self.debug_info.attach_var("%s %s" % (i+1,os.path.basename(m)) )

        for x in xrange(self.n):
            for y in xrange(self.n):
                t = self.tiles[x][y]
                t.draw(self.debug_info)