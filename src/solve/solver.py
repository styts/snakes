import copy
import os
import sys
import pygame
from guppy import hpy
import hashlib
import networkx as nx
import plotter
from src.logic.state import State

class Solver:
    def __init__(self,debug_info=None,quit_on_first=False):
        self.debug_info = debug_info
        self.state = None
        self.gr = None
        self.sols = []
        self.quit_on_first = quit_on_first
        self.MAX_RECURSION_DEPTH = 10000

    def set_state(self,state):
        self.state = copy.copy(state)
        del self.gr
        self.gr = nx.Graph(finals=[])

    def solve(self):
        print "Populating...",
        sys.setrecursionlimit(self.MAX_RECURSION_DEPTH)
        self.gr.graph['finals'] = []
        root_node = self.state.to_json()
        self._populate_graph(self.gr,root_node)

        print "Solving...",
        self.sols = self._solve_graph()

        l_shortest = (len(self.sols[0])-1) if len(self.sols) else None
        print "shortest: %s" % l_shortest,
        print "order: %s" % self.gr.order(),
        self._attach_debugs(shortest=l_shortest)


    def draw_graph(self,filename=None,**kwargs):
        return plotter.save_graph(self.gr,self.state.__hash__(),all_solutions=self.sols,filename=filename,**kwargs)
        
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