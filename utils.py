from networkx.algorithms import approximation as approx
import networkx as nx
import random

'''
This function creates a digraph starting from a file.txt.
@param path_graph: the path (relative or absolute) of the file containing the graph
@type path_graph: <class 'str'>
@return: the digraph G
@rtype: <class 'networkx.classes.digraph.DiGraph'>
'''
def create_graph_from_file(path_graph):
    g=nx.DiGraph()
    with open(path_graph) as f:
        line=random.choice(f.readlines())
        line=line[:len(line)-4]
        line=line.split(' {{')[1].split('}, {')
        for l in line:
            ll=l.split(',')
            n1=ll[0].strip()
            n2=ll[1].strip()
            g.add_edge(int(n1),int(n2))
        return g

'''
This function creates a digraph with networkx random generator. The graph in output is a simple graph, and all its vertices belong to an st-path.
@param min_n: the minimum number of nodes
@type min_n: <class 'int'>
@param max_n: the maximum number of nodes
@type max_n: <class 'int'>
@return: the digraph G
@rtype: <class 'networkx.classes.digraph.DiGraph'>
'''
def create_graph_with_nx_generator(min_n, max_n):
    n=random.randint(min_n, max_n)
    m=random.randint(n, (n-1)+(n-2)*(n-2))
    g=nx.gnm_random_graph(n, m, directed=True)

    g.remove_edges_from(list(g.in_edges(0))) #remove nodes incoming in s
    g.remove_edges_from(list(g.edges(len(g.nodes())-1))) #remove nodes outcoming from t
    g.remove_nodes_from(list(nx.isolates(g))) #remove isolated nodes

    t=len(list(g.nodes()))-1

    if 0 in g.nodes() and t in g.nodes() and approx.node_connectivity(g, 0, t)>0: #remove nodes not in an st-path
        paths=list(nx.all_simple_paths(g, 0, t))
        nodes_ok=[]
        nodes_no=[]
        for path in paths:
            nodes_ok+=path
        for node in g.nodes():
            if node not in nodes_ok:
                nodes_no.append(node)
        g.remove_nodes_from(nodes_no)
        relabel_nodes={}
        for i in list(range(len(list(g.nodes())))):
            relabel_nodes[list(g.nodes())[i]]=i
        g=nx.relabel_nodes(g, relabel_nodes)

    else:
        g=create_graph_with_nx_generator(min_n, max_n)
    return g

''' The function tests if 'edge' is in 'graph'. If 'edge' not in 'graph', the function raises an exception. '''
def is_edge(graph, edge):
    if not graph.has_edge(edge[0], edge[1]):
        raise nx.NetworkXException(str(edge) + ' not in graph' )
    return 

''' The function tests if 'edges' are in 'graph'. If 'edges' not in 'graph', the function raises an exception. '''
def are_edges(graph, edges):
    for edge in edges:
        is_edge(graph, edge)

''' The function tests if 'mes' is minimal, hence if 'mes' is a minimal edge separator and not only an edge separator. '''
def is_minimal(graph, mes):
    are_edges(graph, mes)

    s=0
    t=len(graph.nodes())-1

    if (mes==list(graph.edges(s))): return True
    
    g=graph.copy()
    x=mes.copy()
    
    rem=[]
    for edge in mes:
        x.remove(edge)
        g.remove_edges_from(x)
        if approx.node_connectivity(g, s, t)==0:
            rem.append(edge)
        g=graph.copy()
        x=mes.copy()
            
    return len(rem)==0

