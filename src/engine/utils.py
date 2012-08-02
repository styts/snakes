from threading import Thread
import time
import pygame

TARGETS = ['g','b','y','r'] # Tile.v
SNAKE_VALUES = ['G','B','Y','R','O','P']
colors = {
          "Y" : (255,255,0),
          "G" : (0,255,0),
          "B" : (0,0,255),
          "R" : (255,0,0),
          "O" : (255,102,51),
          "P" : (153,51,153),
          'g' : (0,102,0),
          'b' : (0,0,102),
          'y' : (102,102,0),
          'r' : (102,0,0),
          '0' : (20,20,20),
          '1' : (50,50,50)
          }
              
def patternize_tile(finalSurface, fn):
    """Fills the surface with tiles from filename"""
    """Called once when creating a level backgorund"""
    # adopted from http://www.devshed.com/c/a/Python/PyGame-for-Game-Development-Font-and-Sprites/1/
    
    tileSurface = pygame.image.load(fn)
    tileSurface.convert()

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

def letter_to_color(letter):
    global colors

    if letter not in colors:
        return (0,0,0)
    else:
        return colors[letter]

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