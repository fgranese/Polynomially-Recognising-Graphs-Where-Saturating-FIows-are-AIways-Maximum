from alg2 import *
from alg1 import *
from vgraph import *
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

'''
This is a gui application for viewing graphs. Such graphs may be obtained taking a database in input, or the may be generated by a generator.
The application displays the graph (which is drawn by function in vgraph.py) and shows some informations about the graph.
The gui is realized using Tkinter package. The gui consists of a PanedWindow in which two Buttons are placed, a Canvas in which the drawn of the graph is palced and of another PanedWindow in which the Label with the informations on the graph is placed.
When the user clicks on 'Draw Graph from Database' the graph is directly shown; when the user clicks on 'Draw Graph from Generator' a new window is shown. This window (DIALOG) contains two Labels with two Entries for entering the minimum and the maximum number of nodes for the graph under contruction. Once 'Compute the graph' is clicked the graph is displayed.
'''

WIN=tk.Tk()
WIN.title('Graph Viewer')
w=1000
h=1000
ws=WIN.winfo_screenwidth()
hs=WIN.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
WIN.geometry('%dx%d+%d+%d' % (w, h, x, y))
WIN.wm_iconbitmap("icona.ico")
WIN.focus_set()

f=plt.figure(figsize=(5,4))
a=f.add_subplot(111)

draw_digraph(nx.Graph(), 0, 0)

canvas=FigureCanvasTkAgg(f, master=WIN)
canvas.show()

label_info=Label(WIN, justify=LEFT, font=("Helvetica", 12), wraplength=500)

def show_graph(g):
    s=0
    t=len(g.nodes())-1

    is_edge=is_edge_weak(g)
    is_edge_str='No'
    if (is_edge==False):
        draw_digraph(g, s, t)
    else:
        draw_digraph(g, s, t, is_edge[1], is_edge[2])
        is_edge_str='Yes.\n'+'- In the graph there exists the path: \n'+str(is_edge[1])+'\n'+'- The path passes twice through the mes: \n'+str(is_edge[2])

    canvas.draw()

    label_info['text']='Number of node: '+str(len(g.nodes()))+'\n'+'Number of edges: '+str(len(g.edges()))+'\n'+'The graph is edge-weak? '+is_edge_str
    
def new_graph_from_bd():
    a.clear()
    filename = filedialog.askopenfilename(filetypes = (("Text files", "*.txt"),("All files", "*.*") ))
    g=create_graph_from_file(filename)
    show_graph(g)    
    
def choose_min_max_node():
    DIALOG=tk.Tk()
    DIALOG.title('Choosing number of nodes')
    DIALOG.resizable(False, False)
    w=400
    h=200
    ws=WIN.winfo_screenwidth()
    hs=WIN.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    DIALOG.geometry('%dx%d+%d+%d' % (w, h, x, y))
    DIALOG.wm_iconbitmap("icona.ico")
    DIALOG.focus_set()

    labelframe=LabelFrame(DIALOG, bg='white', relief = FLAT)
    labelframe.pack(fill = "both", expand = "yes")
    label_message=Label(labelframe, bg='white', justify=LEFT, text='\n Please enter the minimum and the maximum number of nodes  \n to compute the graph \n')
    label_message.pack(side=tk.TOP)

    label_entry_min=PanedWindow(DIALOG)
    label_min=Label(label_entry_min, text='Minimum number of nodes (>1): ')
    label_min.pack(side=LEFT)
    content = StringVar()
    entry_min=Entry(label_entry_min, bd=3, textvariable=content)
    entry_min.pack(side=RIGHT)
    label_entry_min.add(label_min)
    label_entry_min.add(entry_min)
    label_entry_min.pack(fill=tk.BOTH, expand=1)
    
    label_entry_max=PanedWindow(DIALOG)
    label_max=Label(label_entry_max, text='Maximum number of nodes (>1): ')
    label_max.pack(side=LEFT)
    entry_max=Entry(label_entry_max, bd=3)
    entry_max.pack(side=RIGHT)
    label_entry_max.add(label_max)
    label_entry_max.add(entry_max)
    label_entry_max.pack(fill=tk.BOTH, expand=1)

    def callback():
        s_min=entry_min.get()
        s_max=entry_max.get()
        if s_min.isdigit() and s_max.isdigit():
            min_n=int(s_min)
            max_n=int(s_max)
            if min_n>1 and min_n<=max_n:
                print(min_n, max_n)
                DIALOG.destroy()
                new_graph_from_generator(min_n, max_n)
        
    button_ok=tk.Button(DIALOG, text="Compute the graph", command=callback)
    button_ok.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
    
def new_graph_from_generator(min_n, max_n):
    a.clear()
    g=create_graph_with_nx_generator(min_n, max_n)
    show_graph(g)

buttons_pained=PanedWindow()

graph_db=tk.Button(buttons_pained, text="Draw Graph from Database", command=new_graph_from_bd, font=("Helvetica", 12))
graph_gen=tk.Button(buttons_pained, text="Draw Graph from Generator", command=choose_min_max_node, font=("Helvetica", 12))

buttons_pained.add(graph_db)
buttons_pained.add(graph_gen)

buttons_pained.pack(side=tk.TOP)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
label_info.pack()

tk.mainloop()


