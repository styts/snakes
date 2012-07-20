from guppy import hpy #@UnresolvedImport
from logic.state import State
from logic.map import Map
from logic.snake import Snake
from solver import Solver
import pprint
import gc

def main():
    #gc.set_debug(gc.DEBUG_LEAK)
    
    
    h = hpy()
    h.setrelheap()

    coords = Map.load_coords("4x4-2.png")
    map = Map(coords['tiles'])
    s = State(map,Snake.make_snakes(map,coords['snakes']))
    solver = Solver()
    solver.set_state(s)
    
    #del solver
    #del s
    #del map
    
    print h.heap()
    
    pprint.pprint(gc.garbage)

main()