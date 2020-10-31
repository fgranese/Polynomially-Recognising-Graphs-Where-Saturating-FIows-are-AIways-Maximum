from networkx.algorithms import approximation as approx
from utils import *
import networkx as nx
import random

'''
The function computes (G_s)^edges.
@param graph: the digraph on which the subgraph (G_s)^edges is computed
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param edges: the set of edges to remove from graph
@type edges: <class 'list'>
@return: the digraph (G_s)^edges
@rtype: <class 'networkx.classes.digraph.DiGraph'>
@raise: networkx.NetworkXException if graph not contains edges
'''
def compute_gs(graph, edges):
    are_edges(graph, edges)

    s=0
    graph.remove_edges_from(edges)

    g=nx.DiGraph()
    g.add_edges_from(graph.edges(s))
    for e in graph.edges():
        if e[0]!=s and approx.node_connectivity(graph, s, e[0])>0: #edges reachable from s
            g.add_edge(e[0], e[1])
    return g

'''
The function tests if all paths from s to 'edge' pass through 'set_e'.
@param graph: the starting digraph 
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param set_e: the set of edges on which the edge-precedence is tested
@type set_e: <class 'list'>
@param edge: the edge on which the edge-precedence is tested
@type edge: <class 'tuple'>
@return: True if edge is preceded by set_e, False otherwise
@rtype: <class 'bool'>
@raise: networkx.NetworkXException if graph not contains edge or set_e
'''
def edge_prec(graph, set_e, edge):
    are_edges(graph, set_e)
    is_edge(graph, edge)
    
    s=0

    if edge in set_e: return True
    if edge[0]==s and edge not in set_e: return False

    paths = nx.all_simple_paths(graph, s, target=edge[0])
    m=map(nx.utils.pairwise, paths) #paths expressed in edges
    for path in m:
        l=list(path)
        inter=[e for e in l if e not in set_e]
        if inter==l:
            return False
    return True

'''
The function tests if all paths from s to each edge in 'edge_s1' pass through 'edge_s2'.
@param graph: the starting digraph 
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param edge_s1: the set of edges on which the edges set-precedence is tested
@type edge_s1: <class 'list'>
@param edge_s2: the set of edges on which the edges set-precedence is tested
@type edge_s2: <class 'list'>
@return: True if edge_s1 is preceded by edge_s2, False otherwise
@rtype: <class 'bool'>
@raise: networkx.NetworkXException if graph not contains edge_s1 or edge_s2
'''
def edge_set_prec(graph, edge_s1, edge_s2):
    are_edges(graph, edge_s1)
    are_edges(graph, edge_s2)
    
    is_in=[]
    for edge in edge_s1:
        is_in.append(edge_prec(graph, edge_s2, edge))

    if False not in is_in:
        return True
    return False

'''
The function computes the immediate predecessor of 'mes' with respect to 'edge' in 'graph'.
@param graph: the starting digraph 
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param mes: the mes of which the immediate predecessor is computed
@type mes: <class 'list'>
@param edge: the edge under which the predecessor of mes is computed
@type edge: <class 'tuple'>
@return: the immediate predecessor of mes^edge
@rtype: <class 'list'>
@raise: networkx.NetworkXException if graph not contains mes or the mes is not minimal
'''        
def predecessor_mes_edge(graph, mes, edge):
    if not is_minimal(graph, mes): raise nx.NetworkXException(str(mes) + ' is not a minimal edge-separator')

    s=0
    t=len(graph.nodes())-1

    out_s=list(graph.edges(s)) #edges outgoing from s
    if edge in out_s: return mes #an edge incidents to s has not predecessors

    x_e_prev=mes+list(graph.in_edges(edge[0]))
    x_e_prev.remove(edge) #(X\{e}) U prev(e)

    g=graph.copy() #deep copy
    g_s=compute_gs(g, x_e_prev) #(G_s)^((X\{e}) U prev(e))

    i_s=[] #I_s((X\{e}) U prev(e))
    ed_g=list(graph.edges())
    ed_gs=list(g_s.edges())

    for e in x_e_prev:
        prev_e=list(graph.in_edges(e[0]))
        l=[e2 for e2 in prev_e if e2 not in ed_gs]
        if len(l)==len(prev_e) and e not in out_s:
            i_s.append(e)

    mes_l=[e for e in x_e_prev if e not in i_s] #((X\{e}) U prev(e))\I_s((X\{e}) U prev(e))
    return mes_l

'''
The function computes an 'edge'-minimal mes smaller (w.r.t. set-coverage) than 'mes'.
@param graph: the starting digraph 
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param mes: the mes of which the 'edge'-minimal mes is computed
@type mes: <class 'list'>
@param edge: the edge under which the 'edge'-minimal mes is computed
@type edge: <class 'tuple'>
@return: 'edge'-minimal mes 
@rtype: <class 'list'>
'''    
def minimal_mes(graph, mes, edge):
    x=mes.copy()
    a=__compute_a__(graph, x, edge)
    while len(a)>0:
        f=a[random.randint(0, len(a)-1)]
        x1=predecessor_mes_edge(graph, x, f) #X^f
        x=x1.copy()
        a=__compute_a__(graph, x, edge)
    return x

''' The function computes the set A={f in 'mes' | f not in out(s) and ('mes' U prev(f))\{'edge'} not precedes 'edge'}. '''
def __compute_a__(graph, mes, edge):
    s=0
    out_s=list(graph.edges(s))
    a=[]
    for f in mes:
        if f not in out_s:
            prev_edge=list(graph.in_edges(f[0]))
            x_f_prev=mes+prev_edge
            x_f_prev.remove(edge)

            if not edge_prec(graph, x_f_prev, edge):
                a.append(f)
    return a
