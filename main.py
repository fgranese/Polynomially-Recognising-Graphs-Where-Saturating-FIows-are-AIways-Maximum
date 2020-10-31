from alg2 import *
from alg1 import *
from vgraph import *

def test1():
    i=0
    ll=[]
    j=1
    while i<400:
        g=create_graph_with_nx_generator(6, 6)
        if len(g.nodes())==6 and len(g.edges())==6 and set(g.edges()) not in ll:
            print(j, is_edge_weak(g))
            j+=1
            ll.append(set(g.edges()))
        i+=1

def test():
    ll=[]
    gg=[]
    x=-1
    edges=4
    i=0
    while i<500000:
        x=len(ll)
        g=create_graph_with_nx_generator(7, 7)
        while len(g.nodes())!=7 or len(g.edges())!=7 or set(g.edges()) in ll:
            g=create_graph_with_nx_generator(7, 7)
        i+=1
        ll.append(set(g.edges()))
        print(len(ll), is_edge_weak(g))
        

def test2():
    g=create_graph_from_file('graph.txt')
    #g=create_graph_with_nx_generator(20, 30)
    d=st_minimal_edge_separators(g)
    for u, v in d.items():
        print('LIVELLO', u)
        i=1
        for mes in v:
            print(i, ':', mes)
            i+=1

def test3():
    g=create_graph_from_file('graph.txt')
    #g=create_graph_with_nx_generator(10,10)
    s=0
    t=len(g.nodes())-1
    is_edge=is_edge_weak(g)
    if (is_edge==False):
        #draw_digraph(g, s, t)
        print(is_edge)
    else:
        print(is_edge)
        #draw_digraph(g, s, t, is_edge[1], is_edge[2])
    
    
def main():
    test2()
                
                
    
    
    

if __name__ == "__main__":
    main()
 
