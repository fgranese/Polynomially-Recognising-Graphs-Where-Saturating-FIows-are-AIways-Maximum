from networkx.algorithms import approximation as approx
from alg4 import *
from utils import *
import networkx as nx
import random
    
'''
The function computes the immediate successor of 'mes' with respect to 'edge' in 'graph'. 
@param graph: the starting digraph 
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@param mes: the mes of which the immediate successor is computed
@type mes: <class 'list'>
@param edge: the edge under which the successor of mes is computed
@type edge: <class 'tuple'>
@return: the immediate successor of mes_edge
@rtype: <class 'list'>
@raise: networkx.NetworkXException if graph not contains mes or the mes is not minimal
''' 
def successor_mes_edge(graph, mes, edge):
    if not is_minimal(graph, mes): raise nx.NetworkXException(str(mes) + ' is not a minimal edge-separator')
    
    s=0
    t=len(graph.nodes())-1

    in_t=list(graph.in_edges(t)) #edges incoming in t
    if edge in in_t: return mes #an edge incidents to t has no successors

    x_e_next=mes+(list(graph.edges(edge[1])))
    x_e_next.remove(edge) #(X\{e}) U next(e)

    g=graph.copy() #deep copy
    g_t=compute_gt(g, x_e_next) #(G_t)^((X\{e}) U next(e))

    i_t=[] #I_t((X\{e}) U next(e))
    ed_g=list(g.edges())
    ed_gt=list(g_t.edges())

    for e in x_e_next:
        next_e=list(graph.edges(e[1]))
        l=[e2 for e2 in next_e if e2 not in ed_gt]
        if len(l)==len(next_e) and e not in in_t:
            i_t.append(e) 

    mes_r=[e for e in x_e_next if e not in i_t] #((X\{e}) U next(e))\#I_t((X\{e}) U next(e))
    return mes_r 

'''
The function computes the set of all minimal edge separators in 'graph'. The number of keys of the dictionary, containing all these mes, is equal to the maximum number of levels in 'graph', that is equal to the shortest path from s to t.
@param graph: the starting digraph of which the set of all minimal edge separators is computed
@type graph: <class 'networkx.classes.digraph.DiGraph'>
@return: the dictionary having as key the integers indicating the level of the minimal edge separators, and as values the list of minimal edge separators
@rtype: <class 'dict'>
''' 
def st_minimal_edge_separators(graph):
    s=0
    t=len(graph.nodes())-1

    max_lev=0 #number of levels
    temp_lev=0
    in_t=list(graph.in_edges(t)) #edges entering in t
    for edge in in_t:
        if edge[0]!=0 and approx.node_connectivity(graph, 0, edge[0])>0:
            temp_lev=nx.shortest_path_length(graph, 0, edge[0])
            if temp_lev>max_lev:
                max_lev=temp_lev

    L={} #dict containing all mes
    i=0
    while i<=max_lev+1:
        L[i]=[]
        i+=1

    out_s=graph.edges(s) 

    j=0
    L[j]+=[set(out_s)]

    while j<=max_lev:
        l_j=L[j].copy() #L_j
        l_j1=L[(j+1)].copy() #L_j+1
        len_lj=len(l_j)

        l_j_j1=__st_minimal_edge_separators_aux__(graph, l_j.copy(), l_j, l_j1, j)

        for mes in l_j_j1[0]: #mes in L_j
            if mes not in L[j]:
                L[j].append(mes)
        for mes in l_j_j1[1]: #mes in L_j+1
            if mes not in L[(j+1)]:
                L[(j+1)].append(mes)       

        if len_lj==len(L[j]): #no new mes are added to L_j hence all mes in L_j were examined
            j+=1

    for mes in L[(max_lev+1)]: 
        if mes not in L[max_lev]:
            L[(max_lev)]+=[mes]
    del L[(max_lev+1)]
    return L

''' The function  computes all immediate successors of all minimal edge separators in 'l' and puts each computed mes either in 'l_j' or in '_j1' with respect to 'j'. The function returns a tuple with 'l_j' and 'l_j1' (containing the computed mes).'''
def __st_minimal_edge_separators_aux__(graph, l, l_j, l_j1, j):
    s=0
    t=len(graph.nodes())-1

    for mes in l:
        for edge in mes:
            h_e=nx.shortest_path_length(graph, s, edge[0]) #distance from s to edge
            mes_r=set(successor_mes_edge(graph, list(mes), edge)) #immediate successor of mes with respect to edge

            if mes_r not in l_j+l_j1: #mes_r must not be just computed
                if h_e==j:
                    l_j1.append(mes_r)
                else:
                    l_j.append(mes_r)

    return (l_j, l_j1)

    




















         
