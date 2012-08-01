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


class Solver:
    def __init__(self,debug_info=None,quit_on_first=False,save_tmp=True,use_temp=True,use_cloud=False):
        self.debug_info = debug_info
        self.state = None
        self.gr = None
        self.sols = []
        self.save_tmp=save_tmp
        self.use_temp=use_temp # bypass the solving, just draw?
        self.use_cloud=use_cloud
        self.quit_on_first = quit_on_first
        self.MAX_RECURSION_DEPTH = 1000000

        # create tmp pickle dir if not exist
        td = os.path.join("data","graphs")
        if not os.path.exists(td):
            os.makedirs(td)
        self.tempdir = td

        # make pickling work when called from GUI (on Surface object)
        #import copy_reg
        #copy_reg.pickle(pygame.Surface,lambda x: [])

    def set_state(self,state):
        self.state = copy.copy(state)
        del self.gr
        self.gr = nx.Graph(finals=[])

    def solve(self):
        # load plckled object if possible, otherwise compute(populate and solve) graph
        tmp_pickle = os.path.join(self.tempdir,"%s.pickle" % self.state.__hash__())

        if os.path.exists(tmp_pickle) and self.use_temp:
            # unpickle existing solution graph
            (tmp_gr, tmp_sols) = pickle.load(open(tmp_pickle,'rb'))
            self.gr = tmp_gr
            self.sols = tmp_sols
            del tmp_gr, tmp_sols
            print "Unpickled ", tmp_pickle
        else:
            # solve graph form inital state
            print "Populating...",
            sys.setrecursionlimit(self.MAX_RECURSION_DEPTH)
            self.gr.graph['finals'] = []
            root_node = self.state.to_json()
            self._populate_graph(self.gr,root_node)

            print "Solving...",
            self.sols = self._solve_graph()

        self.l_shortest = (len(self.sols[0])-1) if len(self.sols) else None
        print "shortest: %s" % self.l_shortest,
        print "order: %s" % self.gr.order()
        self._attach_debugs(shortest=self.l_shortest) # continuous visual display of solving progress

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
        
    def _attach_debugs(self,depth=None,shortest=None):
        """Used by the GUI"""
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
    def _populate_graph(self,gr,sxp,depth=0,max_depth=0,found_new=0,has_one=False):
        """Recursively called"""

        if max_depth and depth >= max_depth:
            return 3

        # its a try-catch so that no 'video system not initalized' error comes when running in console mode
        try:
            # process message queue
            pygame.event.pump()
        except pygame.error:
            pass

        sxp_digest = hashlib.md5(sxp).hexdigest()

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

        self._attach_debugs(depth)

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
            if has_one and self.quit_on_first:
                return 42

        for nsx in nssx:
            if not found_new: # if no new neighbours were found during the previous iteration
                return 7
            if self.quit_on_first and len(gr.graph['finals']) and not max_depth:
                return 8
            self._populate_graph(gr,nsx,depth=depth+1,max_depth=max_depth,found_new=found_new) # recurse


    def _solve_graph(self):
        sols = []
        j = self.state.to_json()
        d = hashlib.md5(j).hexdigest()
        for a,p in nx.single_source_shortest_path(self.gr,d).items():
            if a in self.gr.graph['finals']:
                sols.append(p)
        sols = sorted(sols, key=lambda sol: len(sol))
        return sols