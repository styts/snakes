import copy
import os
import sys
import pygame #@UnresolvedImport
from guppy import hpy #@UnresolvedImport
import hashlib

try:
    import matplotlib.pyplot as plt #@UnresolvedImport
except:
    pass #IGNORE:W0702 we don't need the plotter in exe
import networkx as nx #@UnresolvedImport

class Solver:
    def __init__(self,debug_info=None):
        self.debug_info = debug_info
        self.state = None
        self.gr = None

    def do_populate(self,quit_on_first=False):
        MAX_RECURSION_DEPTH = 10000
        recursionlimit = sys.getrecursionlimit()
        print "Rec. limit: ", recursionlimit
        sys.setrecursionlimit(MAX_RECURSION_DEPTH)
        recursionlimit = sys.getrecursionlimit()
        print "Rec. limit: ", recursionlimit
        self.gr.graph['finals'] = []

        node = self.state.to_json()
        self.populate_graph(self.gr,node,quit_on_first=quit_on_first) #quit_on_first=False
        #sys.setrecursionlimit(recursionlimit)

    def attach_debugs(self,depth=None,shortest=None):
        if self.debug_info:
            self.debug_info.attach_var("solver_1","Solver")
            self.debug_info.attach_var("solver_2","======")
            if depth:
                self.debug_info.attach_var("solver_depth","depth: %s" % depth)
            self.debug_info.attach_var("solver_order","order: %s" % self.gr.order())
            self.debug_info.attach_var("solver_finals","finals: %s" % self.gr.graph['finals'].__len__())
            if shortest:
                self.debug_info.attach_var("solver_shortest","shortest: %s" % shortest)
            self.debug_info.attach_var("solver_","")

    #@staticmethod
    def populate_graph(self,gr,sxp,depth=0,max_depth=0,found_new=0,quit_on_first=False,has_one=False):
        #print "order", gr.order()
        #if gr.order() >= 2500:
            #import objgraph
            #objgraph.show_refs([gr], filename='sample-graph.png')
            #objgraph.show_most_common_types(limit=50)
            #objgraph.show_growth()
            #sys.exit(0)

        from logic.state import State
        if max_depth and depth >= max_depth:
            return 3
        # process message queue
        #try:
        pygame.event.pump()
        #except pygame.error:
            #print e
            #pass

        sxp_digest = hashlib.md5(sxp).hexdigest()

        #if not gr.has_node(sxp_digest):
        #    gr.add_nodes_from(sxp_digest)
        found_new = 0
        s = State()
        s.load_from_json(sxp)
        nss = s.get_neighbour_states()
        nssx = []
        completed = []
        for ns in nss:
            j = ns.to_json()
            nssx.append(j)
            if ns.is_complete():
                completed.append(j)
            del ns
        del nss
        del s
        #print "%s\n"%s


        self.attach_debugs(depth)

        for nsx in nssx:
            digest = hashlib.md5(nsx).hexdigest()
            if not gr.has_node(digest):
                gr.add_nodes_from([digest])
                found_new = found_new + 1
                if nsx in completed:
                    gr.node[digest]['complete'] = True
                    has_one = True
                    gr.graph['finals'].append(digest)
            if not gr.has_edge(sxp_digest,digest):
                gr.add_edge(sxp_digest,digest)
            if has_one and quit_on_first:
                return 42

        for nsx in nssx:
            if not found_new: # if no new neighbours were found during the previous iteration
                return 7
            if quit_on_first and len(gr.graph['finals']) and not max_depth:
                return 8
            self.populate_graph(gr,nsx,depth=depth+1,max_depth=max_depth,found_new=found_new,quit_on_first=quit_on_first) # recurse


    def solve(self,heapy=False,print_debug=False,draw_graph=False,quit_on_first=False):
        if print_debug: print "Populating..."
        if heapy:
            h = hpy()
            h.setrelheap()
        self.do_populate(quit_on_first=quit_on_first)
        if print_debug:
            print "done"
            print "Solving...",
        sols = self.solve_graph()
        #print sols

        l_shortest = (len(sols[0])-1) if len(sols) else None
        if print_debug:
            print "shortest: %s" % l_shortest
            print "Order: %s" % self.gr.order()

        try:
            if draw_graph: Solver.draw_graph(self.gr,self.state.to_json(),all_solutions=sols)
        except:
            pass #IGNORE:W0702 dont use plt in exe

        self.attach_debugs(shortest=l_shortest)
        del self.gr
        if heapy: print h.heap()
        return sols

    def set_state(self,state):
        self.state = copy.copy(state)
        del self.gr
        self.gr = nx.Graph(finals=[])

    @staticmethod
    def draw_graph(gr,s=None,all_solutions=[]): #IGNORE:W0102
        print "Drawing...",
        plt.figure(1,figsize=(20,15))

        sols = all_solutions[0] if len(all_solutions) else None

        # not all labels should be displayed, only those that are part of the solution
        labels = {}
        #labels_anyway = True
        labels_anyway = False
        if sols or labels_anyway:
            for n in gr.nodes():
                if not labels_anyway and n not in sols:
                    labels[n] = ""
                else:
                    labels[n] = str(n)

        # labels for length of shortest path to each final node
        final_labels = {}
        for s in all_solutions:
            for i in range(len(s)):
                n = s[i]
                if i == len(s)-1:
                    final_labels[n] = len(s)-1
        # assign edges to path (to draw highlighted)
        if sols:
            path = []
            for i in range(len(sols)-1):
                u = sols[i]
                v = sols[i+1]
                e = (u,v)
                path.append(e)
        #pos=nx.graphviz_layout(gr,prog='dot') #/*,overlap="compress"*/
        #pos=nx.graphviz_layout(gr,prog='dot',overlap="compress")
        pos=nx.pygraphviz_layout(gr)

        #pos=nx.spring_layout(gr) # too unstructured

        #pos=nx.spectral_layout(gr) # too compressed

        #pos=nx.shell_layout(gr)# all nodes are on a cirlce , wtf
        #pos=nx.circular_layout(gr)# all nodes are on a cirlce , wtf

        if sols:
            # begin
            nx.draw(gr,pos,edgelist=[],nodelist=[sols[0]],node_size=500,alpha=0.5,node_color='b',with_labels=False)
            # finals
            nx.draw(gr,pos,edgelist=[],nodelist=gr.graph['finals'],node_size=100,alpha=0.5,node_color='y',labels=final_labels)
            # end
            nx.draw(gr,pos,edgelist=[],nodelist=[sols[len(sols)-1]],node_size=500,alpha=0.5,node_color='g',with_labels=False)
            # path
            nx.draw(gr,pos,edgelist=path,nodelist=sols,width=3,node_size=10,alpha=0.5,edge_color='r',font_family="monospace",font_size=12,with_labels=False)
        # all the nodes with labels along path only
        # with_labels=(sols and len(sols)<1000),labels=labels if sols else None
        nx.draw(gr,pos,node_size=2,alpha=0.2,root=s,font_family="monospace",font_size=11,with_labels=False,labels=labels)

        fn =os.path.join("data","graphs","graph.png")
        plt.savefig(fn)
        plt.close()
        print "done"


    def solve_graph(self):
        sols = []
        j = self.state.to_json()
        d = hashlib.md5(j).hexdigest()
        for a,p in nx.single_source_shortest_path(self.gr,d).items():
            if a in self.gr.graph['finals']:
                sols.append(p)
        sols = sorted(sols, key=lambda sol: len(sol)) #IGNORE:W0108
        return sols

def main():
    print "Solver"

if __name__ == "__main__":
    main()
