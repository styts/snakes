from src.logic.state import State
from src.solve.solver import Solver

#import gc
#gc.set_debug(gc.DEBUG_LEAK)

#fn = 'data/maps/340_4-10.json' # ez
#fn = 'data/maps/8188_3-21.json' # hard
fn = 'data/maps/19736_3-15.json' # hard

s = State()
slv = Solver(ignore_pickle=True)
s.load_from_json_file(fn)
slv.set_state(s)
sols = slv.solve()
slv.draw_graph(size=(8,6))
