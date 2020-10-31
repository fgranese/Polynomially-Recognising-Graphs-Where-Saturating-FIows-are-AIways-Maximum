from utils import *
from alg3 import *
from alg4 import *

'''
The function tests  if 'graph' is edge-weak. If 'graph' is edge-weak the function returns a tuple. Such a tuple contains a bool value (True), a list (the path) and another list (the mes that is touched twice by the path). This choice of return type is done for facilitating the edge-weakness visualization of the graph.
@param graph: the starting digraph
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@return: False if the graph is not edge-weak, (True, path, mes) otherwise
@rtype: <'bool'> / <'tuple'>
'''
def is_edge_weak(graph):
    s=0
    t=len(list(graph.nodes()))-1

    mes=list(graph.edges(s)) #first mes of every chain
    in_t=list(graph.in_edges(t)) #last mes of every chain

    while mes!=in_t:
        mes_r=immediate_mes_right(graph, mes) #an immediate successor of 'mes'
        bool_path=__is_edge_critical__(graph, mes_r)
        if bool_path[0]==True:
            return (True, bool_path[1], mes_r)

        diff=[e for e in mes_r if e not in mes] #e in X\X'
        for e in diff:
            mes_m=minimal_mes(graph, mes_r, e) #X*
            bool_path=__is_edge_critical__(graph, mes_m)
            if bool_path[0]==True:
                return (True, bool_path[1], mes_m)

        if mes!=mes_r:
            mes=mes_r
        else:
            break
    return False

''' The function tests if there exists a path between two edges of 'mes' in 'graph' '''
def __is_edge_critical__(graph, mes):
    for edge in mes:
        for edge1 in mes:
            if edge!=edge1 and (approx.node_connectivity(graph, edge[1], edge1[0])>0): 
                paths = nx.all_simple_paths(graph, edge[1], edge1[0]) 
                m=map(nx.utils.pairwise, paths) #paths expressed in edges
                ll=[]
                for path in m:
                    l=[edge]
                    l+=list(path)
                    l.append(edge1)
                    ll.append(l)
                return (True, ll[random.randint(0, len(ll)-1)])
    return (False, [])
