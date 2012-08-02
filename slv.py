#from src.logic.state import State
#from src.solve.solver import Solver
from src.solve.utils import process_json
#import gc
#gc.set_debug(gc.DEBUG_LEAK)

#fn = 'data/maps/340_4-10.json' # ez
fn = 'data/maps/8188_3-21.json' # hard
#fn = 'data/maps/19736_3-15.json' # hard
j="".join(open(fn,'r').readlines())
print j
process_json(j, False, ignore_pickle=True)

#s = State()
#slv = Solver(ignore_pickle=True)
#s.load_from_json_file(fn)
#slv.set_state(s)
#sols = slv.solve()
#slv.draw_graph(size=(8,6))
