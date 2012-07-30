from threading import Thread
import time
#from guppy import hpy #@UnresolvedImport

TARGETS = ['g']
SNAKE_VALUES = ['G','B','Y','R','O','P']

def letter_to_color(letter):
    colors = {
              "Y" : (255,255,0),
              "G" : (0,255,0),
              "B" : (0,0,255),
              "R" : (255,0,0),
              "O" : (255,102,51),
              "P" : (153,51,153),
              'g' : (0,102,0),
              '0' : (20,20,20),
              '1' : (50,50,50)
              }
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
            self.solver.draw_graph("data/graphs/graph-%s.png" % self.solver.state.__hash__())
        print "Took %d seconds" % int(time.time() - self.t)



def solve(state,debug_info=False,quit_on_first=False,draw_graph=True):
    st = _SolverThread(state,draw_graph,quit_on_first,debug_info)
    st.start()


# import pickle
# def get_pickling_errors(obj,seen=None):
#     if seen == None:
#         seen = []
#     try:
#         state = obj.__getstate__()
#     except AttributeError:
#         return
#     if state == None:
#         return
#     if isinstance(state,tuple):
#         if not isinstance(state[0],dict):
#             state=state[1]
#         else:
#             state=state[0].update(state[1])
#     result = {}    
#     for i in state:
#         try:
#             pickle.dumps(state[i],protocol=2)
#         except pickle.PicklingError:
#             if not state[i] in seen:
#                 seen.append(state[i])
#                 result[i]=get_pickling_errors(state[i],seen)
#     return result