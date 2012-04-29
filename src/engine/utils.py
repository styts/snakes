from solver import Solver
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

class SolverThread(Thread):
    def __init__(self,state,draw_graph,quit_on_first,debug_info):
        Thread.__init__(self)
        #self.debug_info = debug_info
        self.draw_graph = draw_graph
        self.quit_on_first = quit_on_first
        self.t = time.time()
        self.solver = Solver(debug_info)
        self.solver.set_state(state)
    def run(self):
#        h = hpy()
#        h.setrelheap()
        self.solver.solve(heapy=False,print_debug=True,draw_graph=self.draw_graph,quit_on_first=self.quit_on_first)
        print "Took %d seconds" % int(time.time() - self.t)
#        print h.heap()

def solve(state,debug_info=False,quit_on_first=False,draw_graph=False):
    st = SolverThread(state,draw_graph,quit_on_first,debug_info)
    st.start()
#    t = time.time()
#    solver = Solver()
#    solver.set_state(state)
#    solver.solve(heapy=False,print_debug=True,draw_graph=draw_graph,quit_on_first=quit_on_first)
#    del solver
#    print "Took %d seconds" % int(time.time() - t)
