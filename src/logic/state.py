import copy
from map import Map
from snake import Snake
import pygame #@UnresolvedImport
import json
import hashlib


class State:
    def __repr__(self):
        return "%s" % str(self.map) #.replace("\n", "\\n")
        #return "map.tiles[1][0]: %s, complete: %s" % (self.map.tiles[1][0],self.is_complete())

    def __init__(self,map=None,snakes=None,parent_state=None): # IGNORE:W0622
        self.move = None
        self.map = map
        self.snakes = snakes
        self.parent_state = parent_state

    def load_from_json(self,string,is_struct=False):
        if not is_struct:
            struct = json.loads(string)
        else:
            struct = string
        self.map = Map(coordinates=struct['map'])
        self.snakes = []
        for sj in struct['snakes']:
            snake = Snake(self.map, sj['color'], None)
            snake.elements = Snake.make_elements(sj['elements'],snake)
            snake.assign_to_tiles()
            self.snakes.append(snake)

    def set_surface(self,surface):
        self.map.set_surface(surface)
        for s in self.snakes:
            s.set_surface(surface)

    def load_from_json_file(self,fn):
        fp = open(fn,'r')
        string = "\n".join(fp.readlines())
        self.load_from_json(string)

    def load_from_file(self,map_name):
        coords = Map.load_coords(map_name)
        self.map = Map(coordinates=coords['tiles'])#IGNORE:W0622
        self.snakes = Snake.make_snakes(self.map,coords['snakes'])

    def __copy__(self):
        """
        m = Map(coordinates=self.map.get_coords())
        ss = Snake.make_snakes(m,self.map.get_coords(snakes=True))
        """
        s = State()
        s.load_from_json(self.to_json())
        s.parent_state = self
        return s

    def __eq__(self,other):
        return str(self.map) == str(other.map)

    def __hash__(self):
        # http://kodeclutz.blogspot.com/2008/08/custom-hash-objects-in-python.html
        # the hash of our string is our unique hash
        #return hash(str(self.map))

        # the above gives just numbers...
        # use this:
        m = hashlib.md5()
        m.update(str(self.map))
        str_md5 = m.hexdigest()
        return str_md5

    def get_neighbour_states(self,exclude=[]):#IGNORE:W0102
        ns = []
        for s in self.snakes:
            for m in s.get_moves():
                newstate = State.apply_move(self,m)
                if newstate not in exclude:
                    ns.append(newstate)
                    #exclude.append(newstate) # hmmm try
        return ns

    @staticmethod
    def apply_move(state,m):
        n = copy.copy(state)
        t = n.map.get_tile(m.x1,m.y1)
        if t.se:
            t.se.move(m)
            n.move = m
        return n

    def is_complete(self):
        "a state is complete, when all end tiles are complete"
        return self.map.is_complete()

    def get_thumbnail(self):
        surf = pygame.Surface((self.map.n,self.map.n))
        surf.lock()
        for x in xrange(self.map.n):
            for y in xrange(self.map.n):
                t = self.map.tiles[x][y]
                c = t.se.snake.color if t.se else t.color
                surf.set_at((x,y),c)
        surf.unlock()
        return surf

    def export(self):
        foo = {}
        foo['map'] = self.map.export()
        foo['snakes'] = []
        for s in self.snakes:
            foo['snakes'].append(s.export())
        return foo

    def to_json(self):
        struct = self.export()
        #print sys.getsizeof(struct)
        jstr = json.dumps(struct)
        #print sys.getsizeof(jstr)
        return jstr

    def save_to_json(self,fn):
        fp = open(fn,'w')
        fp.write(self.to_json())
        fp.close()

    def save_to_image(self,filename):
        n = self.map.n
        surf = pygame.Surface((2*n,n))
        surf.lock()
        for x in xrange(n):
            for y in xrange(n):
                b = self.map.tiles[x][y]
                surf.set_at((x,y),b.color)
                surf.set_at((x+n,y),b.color)
                if b.se:
                    surf.set_at((x+n,y),b.se.snake.color)
        surf.unlock()
        pygame.image.save(surf,filename)

    def __del__(self):
        #print "state deleted"
        del self.map
        for s in self.snakes:
            del s

        pass


