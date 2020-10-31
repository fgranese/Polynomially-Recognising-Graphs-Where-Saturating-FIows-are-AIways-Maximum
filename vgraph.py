import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

'''
This function draw 'graph'. If 'path' and 'mes' are in input, then the function highlights red edges in 'path' and in yellow edges in 'mes'.
@param graph: the graph to draw
@type graph: <class 'networkx.classes.digraph.DiGraph'> 
@param s: the starting node in 'graph'
@type s: <class 'int'>
@param t: the ending node in 'graph'
@type t: <class 'int'>
@param path: the edges in path
@type path: <class 'list'>
@param mes: the edges in mes
@type mes: <class 'int'>
'''
def draw_digraph(graph, s, t, path=None, mes=None):
    pos=nx.circular_layout(graph)

    val_map = {s: 'r', t: 'r'}
    values = [val_map.get(node, 'b') for node in graph.nodes()]

    nx.draw_networkx_nodes(graph, pos, node_color =values, alpha=0.9)
    nx.draw_networkx_edges(graph, pos, edge_color='black', style='dashed', arrows=True)

    if path!=None:
        nx.draw_networkx_edges(graph, pos, edgelist=path, width=2.0, edge_color='red', arrows=True)

    if mes!=None:
        nx.draw_networkx_edges(graph, pos, edgelist=mes, width=3.0, alpha=0.7, edge_color='yellow')

    labels={}
    labels[s]=r'$s$'
    labels[t]=r'$t$'
    for node in graph.nodes():
        if node!=s and node !=t:
            labels[node]=node
            nx.draw_networkx_labels(graph,pos, labels,font_size=16)

    plt.axis('off')


   
    
