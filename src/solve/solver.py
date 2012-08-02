import copy
import os
import sys
import pygame
from guppy import hpy
import hashlib
import networkx as nx
import plotter
from src.logic.state import State
import pickle

#### MEM Profiling
# from IPython import embed
#from pympler import tracker
#tr = tracker.SummaryTracker()
# import objgraph
# from guppy import hpy
# h = hpy()

points = [1] # used by solver, every 'N' new nodes added to graph, do something
N = 200
for o in range(1,500):
    o = N*o
    points.append(o)


class Solver:
    def __init__(self,debug_info=None,quit_on_first=False,save_tmp=True,use_temp=True,use_cloud=False,ignore_pickle=True):
        self.debug_info = debug_info
        self.state = None
        self.gr = None
        self.sols = []
        self.save_tmp=save_tmp
        self.use_temp=use_temp # bypass the solving, just draw?
        self.use_cloud=use_cloud
        self.ignore_pickle = ignore_pickle # don't load a pickle - work for real
        self.quit_on_first = quit_on_first
        self.MAX_RECURSION_DEPTH = 1000000

        # create tmp pickle dir if not exist
        td = os.path.join("data","graphs")
        if not os.path.exists(td):
            os.makedirs(td)
        self.tempdir = td

    def set_state(self,state):
        self.state = copy.copy(state)
        del self.gr
        self.gr = nx.Graph(finals=[])

    #@profile
    def solve(self):
        # load plckled object if possible, otherwise compute(populate and solve) graph
        tmp_pickle = os.path.join(self.tempdir,"%s.pickle" % self.state.__hash__())


        if os.path.exists(tmp_pickle) and self.use_temp and not self.ignore_pickle:
            # unpickle existing solution graph
            (tmp_gr, tmp_sols) = pickle.load(open(tmp_pickle,'rb'))
            self.gr = tmp_gr
            self.sols = tmp_sols
            del tmp_gr, tmp_sols
            print "Unpickled ", tmp_pickle
        else:
            # solve graph form inital state
            print "Populating..."
            if self.quit_on_first:
                print "(will quit on first)"
            sys.setrecursionlimit(self.MAX_RECURSION_DEPTH)
            self.gr.graph['finals'] = []
            Solver._populate_graph(gr=self.gr,root=self.state.to_json(),debug_info=self.debug_info,quit_on_first=self.quit_on_first)

            print "Solving..."
            self.sols = self._solve_graph()

        self.l_shortest = (len(self.sols[0])-1) if len(self.sols) else None
        print "shortest: %s" % self.l_shortest,
        print "order: %s" % self.gr.order()
        Solver._attach_debugs(self.debug_info,self.gr,shortest=self.l_shortest) # continuous visual display of solving progress

        if self.save_tmp and not self.quit_on_first: # only pickle if we're doing a complete computation
            #pickle our object and save it to temp dir
            print "Pickling...",
            #from src.engine.utils import get_pickling_errors
            #print get_pickling_errors(self)
            #del self.state
            pickle.dump( (self.gr, self.sols), open( tmp_pickle, "wb" ))
            print "done"


    def draw_graph(self,filename=None,**kwargs):
        g = plotter.save_graph(self.gr, self.state.__hash__(), all_solutions=self.sols, filename=filename, use_cloud=self.use_cloud, **kwargs)
        if filename and not self.use_cloud:
            os.system("open %s" % filename)
        
    @staticmethod
    def _attach_debugs(debug_info=None,gr=None,depth=None,shortest=None):
        """Used by the GUI"""
        if debug_info:
            debug_info.attach_var("solver_1","Solver")
            debug_info.attach_var("solver_2","======")
            if depth:
                debug_info.attach_var("solver_depth","depth: %s" % depth)
            debug_info.attach_var("solver_order","order: %s" % gr.order())
            debug_info.attach_var("solver_finals","finals: %s" % gr.graph['finals'].__len__())
            if shortest:
                debug_info.attach_var("solver_shortest","shortest: %s" % shortest)
            debug_info.attach_var("solver_","")

    @staticmethod
    #@profile
    def _populate_graph(gr,root,depth=0,max_depth=0,found_new=0,has_one=False,debug_info=None,quit_on_first=None):
        """Recursively called"""
        global points

        #print "%s\t%s" % (gr.order(), depth)
        #print points
        #tr.print_diff()
        o = gr.order(); p0 = points[0]
        if o >= p0:
            points.remove(p0) # so it's only called once
            print "Order >= %s" % p0
            #tr.print_diff()
            #print h.heap()
            # break here and see what's in use
            #pass
            #objgraph.show_growth(limit=10)
            #embed()

        if max_depth and depth >= max_depth:
            return 3

        # its a try-catch so that no 'video system not initalized' error comes when running in console mode
        try:
            # process message queue
            pygame.event.pump()
        except:
            pass

        sxp_digest = hashlib.md5(root).hexdigest()

        found_new = 0
        s = State()
        s.load_from_json(root)
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

        Solver._attach_debugs(debug_info,gr,depth=depth)

        for nsx in nssx:
            digest = hashlib.md5(nsx).hexdigest()
            if not gr.has_node(digest):
                gr.add_nodes_from([digest])
                found_new = found_new + 1
                if nsx in completed:
                    gr.node[digest]['complete'] = True
                    has_one = True
                    gr.graph['finals'].append(digest)
                # else: # once again, drawing will fail if we set this.
                #     gr.node[digest] = None # help with memory? otehrwsise a {} is stored there

            if not gr.has_edge(sxp_digest,digest):
                gr.add_edge(sxp_digest,digest) # attr_dict={} by default. memory. and otherwise drawing does not work
            if has_one and quit_on_first:
                return 42

        for nsx in nssx:
            if not found_new: # if no new neighbours were found during the previous iteration
                return 7
            if quit_on_first and len(gr.graph['finals']) and not max_depth:
                return 8
            Solver._populate_graph(gr,nsx,depth=depth+1,max_depth=max_depth,found_new=found_new,debug_info=debug_info,quit_on_first=quit_on_first) # recurse


    def _solve_graph(self):
        sols = []
        j = self.state.to_json()
        d = hashlib.md5(j).hexdigest()
        for a,p in nx.single_source_shortest_path(self.gr,d).items():
            if a in self.gr.graph['finals']:
                sols.append(p)
        sols = sorted(sols, key=lambda sol: len(sol))
        return sols