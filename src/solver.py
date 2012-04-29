from pygraph.classes.graph import graph #@UnresolvedImport
import copy

class Solver:
    def __init__(self):
        self.state = None
        gr = graph()
    def set_state(self,state):
        self.state = copy.copy(state)
        self.state.map.pprint()
        ns = self.get_neighbour_states()
        #print ns
    def get_neighbour_states(self):
        ns = []
        for s in self.state.snakes:
            for m in s.get_moves():
                newstate = self.state.apply_move(m)
                ns.append(newstate)
        return ns

def main():
    print "Solver"

if __name__ == "__main__":
    main()