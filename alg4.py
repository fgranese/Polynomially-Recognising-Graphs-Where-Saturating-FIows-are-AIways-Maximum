from networkx.algorithms import approximation as approx
from utils import *
import networkx as nx
import random
    
'''
The function computes (G_t)^edges.
@param graph: the digraph on which the subgraph (G_t)^edges is computed
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param edges: the set of edges to remove from graph
@type edges: <class 'list'>
@return: the digraph (G_t)^edges
@rtype: <class 'networkx.classes.digraph.DiGraph'>
@raise: networkx.NetworkXException if graph not contains edges
'''
def compute_gt(graph, edges):
    are_edges(graph, edges)
        
    t=len(graph.nodes())-1
    graph.remove_edges_from(edges)

    g=nx.DiGraph()
    g.add_edges_from(graph.in_edges(t))
    for e in graph.edges():
        if e[1]!=t and approx.node_connectivity(graph, e[1], t)>0: #edges reaching t
            g.add_edge(e[0], e[1])
    return g

'''
The function tests if all paths from 'edge' to t pass through 'set_e'.
@param graph: the starting digraph 
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param set_e: the set of edges on which the edge-coverage is tested
@type set_e: <class 'list'>
@param edge: the edge on which the edge-coverage is tested
@type edge: <class 'tuple'>
@return: True if edge is covered by set_e, False otherwise
@rtype: <class 'bool'>
@raise: networkx.NetworkXException if graph not contains edge or set_e
'''
def edge_cover(graph, set_e, edge):
    are_edges(graph, set_e)
    is_edge(graph, edge)
    
    t=len(graph.nodes())-1
    
    if edge in set_e: return True
    if edge[1]==t and edge not in set_e: return False

    paths = nx.all_simple_paths(graph, edge[1], target=t)
    m=map(nx.utils.pairwise, paths) #paths expressed in edges
    for path in m:
        l=list(path)
        inter=[e for e in l if e not in set_e]
        if inter==l:
            return False
    return True

'''
The function tests if all paths from each edge in 'edge_s1' to t, pass through 'edge_s2'.
@param graph: the starting digraph 
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param edge_s1: the set of edges on which the edges set-coverage is tested
@type edge_s1: <class 'list'>
@param edge_s2: the set of edges on which the edges set-coverage is tested
@type edge_s2: <class 'list'>
@return: True if edge_s1 is covered by edge_s2, False otherwise
@rtype: <class 'bool'>
@raise: networkx.NetworkXException if graph not contains edge_s1 or edge_s2
'''
def edge_set_cover(graph, edge_s1, edge_s2):
    are_edges(graph, edge_s1)
    are_edges(graph, edge_s2)
        
    is_in=[]
    for edge in edge_s1:
        is_in.append(edge_cover(graph, edge_s2, edge))

    if False not in is_in:
        return True
    return False

'''
The function computes all immediate successors of 'mes' and returns one of them.
@param graph: the starting digraph 
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param mes: the mes of which the immediate successor is computed
@type mes: <class 'list'>
@return: the immediate successor of mes
@rtype: <class 'list'>
@raise: networkx.NetworkXException if graph not contains mes or the mes is not minimal
'''
def immediate_mes_right(graph, mes):
    if not is_minimal(graph, mes): raise nx.NetworkXException(str(mes) + ' is not a minimal edge-separator')
    
    s=0
    t=len(graph.nodes())-1

    L=[]
    mes_r=[]
    
    g=graph.copy() #deep copy
    x=mes.copy()

    in_t=list(g.in_edges(t)) #edges incoming in t

    if mes==in_t: return mes #in_t is the last mes in every chain
    diff=[e for e in mes if e not in in_t]

    for e in diff:
        x_e_next=mes+(list(graph.edges(e[1])))
        x_e_next.remove(e) #(X\{e}) U next(e)

        g_t=compute_gt(g, x_e_next) #(G_t)^((X\{e}) U next(e))

        i_t=[] #I_t((X\{e}) U next(e))
        ed_g=list(g.edges())
        ed_gt=list(g_t.edges())

        for e in x_e_next:
            next_e=list(graph.edges(e[1]))
            l=[e2 for e2 in next_e if e2 not in ed_gt]
            if len(l)==len(next_e) and e not in in_t:
                i_t.append(e)

        mes_r=[e for e in x_e_next if e not in i_t] #((X\{e}) U next(e))\I_t((X\{e}) U next(e))
        
        L.append(mes_r)
        mes_r=[]
        x_e_next=[]
        g=graph.copy() #deep copy
        x=mes.copy()

    if len(L)>0:
        X1=L[random.randint(0, len(L)-1)]
        for X in L:
           if edge_set_cover(graph, X, X1):
               X1=X
        return X1
    return []
