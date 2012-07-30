import matplotlib.pyplot as plt
import networkx as nx
import os

def save_graph(gr,start_node=None,all_solutions=[],filename=None,size=(14,9),use_cloud=False):
    print "Drawing...",
    plt.figure(1,figsize=size)

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
        for i in xrange(len(s)):
            n = s[i]
            if i == len(s)-1:
                final_labels[n] = len(s)-1

    # assign edges to path (to draw highlighted)
    if sols:
        path = []
        for i in xrange(len(sols)-1):
            u = sols[i]
            v = sols[i+1]
            e = (u,v)
            path.append(e)

    pos=nx.pygraphviz_layout(gr)
    #pos=nx.graphviz_layout(gr,prog="twopi",root=start_node)
    #pos=nx.graphviz_layout(gr,prog='twopi',args='')
    #pos=nx.spring_layout(gr) # positions for all nodes

    if sols:
        # begin
        nx.draw(gr,pos,edgelist=[],nodelist=[sols[0]],node_size=500,alpha=0.5,node_color='b',with_labels=False)
        # finals
        nx.draw(gr,pos,edgelist=[],nodelist=gr.graph['finals'],node_size=100,alpha=0.5,node_color='y',labels=final_labels)
        # end
        nx.draw(gr,pos,edgelist=[],nodelist=[sols[len(sols)-1]],node_size=500,alpha=0.5,node_color='g',with_labels=False)
        # path
        nx.draw(gr,pos,edgelist=path,nodelist=sols,width=3,node_size=10,alpha=0.5,edge_color='r',font_family="monospace",font_size=10,with_labels=False)

    # all the nodes with labels along path only
    # with_labels=(sols and len(sols)<1000),labels=labels if sols else None
    nx.draw(gr,pos,node_size=2,alpha=0.2,root=start_node,font_family="monospace",font_size=9,with_labels=False,labels=labels)

    print "done drawing"

    # either save file or return plot
    if filename:
        d = os.path.dirname(filename)
        if not os.path.exists(d):
            os.makedirs(d)
        plt.savefig(filename)
        plt.close()

        if use_cloud:
            import cloud
            cloud.files.put(filename)

    else:
        return plt