from threading import Thread
import time
from src.logic.map import Map
from src.logic.snake import Snake
from src.logic.state import State
from src.logic.misc import SNAKE_VALUES


def save_state(state):
    n_s = len(state.snakes)
    n_n = state.map.n
    str_md5 = state.__hash__()
    name = "n%s-s%s-%s" % (n_n, n_s, str_md5)
    #state.save_to_image("data/maps/%s.png" % name)
    state.save_to_json("data/maps/%s.json" % name)


def edit_map(state, event, button):
    if not state:
        return False
    t = state.map.get_tile_at(event.pos[0], event.pos[1])
    if not t:
        return False
    update_snake = button.value in SNAKE_VALUES
    coords = state.map.get_coords()
    if not update_snake:
        coords[t.x][t.y] = button.value
    m = Map(coordinates=coords)
    coords_snakes = state.map.get_coords(snakes=True)
    if update_snake or button.value == '0':
        coords_snakes[t.x][t.y] = button.value
    ss = Snake.make_snakes(m, coords_snakes)
    s = State(m, ss)
    s.save_to_json("data/maps/tempstate.json")
    return True

def patternize_tile(finalSurface, tileSurface):
    """Fills the surface with tiles from filename"""
    """Called once when creating a level backgorund"""
    # adopted from http://www.devshed.com/c/a/Python/PyGame-for-Game-Development-Font-and-Sprites/1/
    
    #tileSurface = pygame.image.load(fn)
    #tileSurface.convert()

    tileRect = tileSurface.get_rect()

    sx, sy = finalSurface.get_size()
    rows = int(sy/tileRect.height) + 1
    columns = int(sx/tileRect.width) + 1

    for y in xrange(rows):
        for x in xrange (columns):
            # Start a new row
            if x == 0 and y > 0:
                # Move the rectangle
                tileRect = tileRect.move([-(columns-1) * tileRect.width, tileRect.height])
            # Continue a row
            if x > 0:
                # Move the rectangle
                tileRect = tileRect.move([tileRect.width, 0])
            finalSurface.blit(tileSurface, tileRect)
    finalSurface.convert()


class _SolverThread(Thread):
    def __init__(self,state,draw_graph,quit_on_first,debug_info):
        Thread.__init__(self)
        self.t = time.time()
        self.draw_graph = draw_graph

        from src.solve.solver import Solver
        self.solver = Solver(debug_info=debug_info,quit_on_first=quit_on_first)
        self.solver.set_state(state)

    def run(self):
        self.solver.solve()
        if self.draw_graph:
            self.solver.draw_graph("data/graphs/graph-%s.png" % self.solver.state.__hash__()) #FIXME remove graph- prefix for consistency
        print "Took %d seconds" % int(time.time() - self.t)

def get_life_values(used_moves, min_moves, max_life, bonus_max):
    safety = max(0, min_moves - used_moves)
    bonus = max(0, min(bonus_max, min_moves + bonus_max - used_moves))
    life = max(0, min(max_life, min_moves + bonus_max + max_life - used_moves))
    r = (life, bonus, safety)
    return r

def solve(state,debug_info=False,quit_on_first=False,draw_graph=True):
    st = _SolverThread(state,draw_graph,quit_on_first,debug_info)
    st.start()