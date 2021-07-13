import matplotlib.pyplot as plt
import squarify
import networkx as nx
from pyvis.network import Network
from random import randint

def square_plot(var,hed,fsize):
    dtn()
    if hed > 1000:
        plt.figure(figsize=(100,50))
    else:
        plt.figure(figsize=(40,20))
    if var == 0:
        counts2 = counts[0].copy()
        counts2["UserName"] = np.where(counts2["Count"].between(0,counts2["Count"][3000]),"",counts2["UserName"])
        squarify.plot(sizes = counts[0]["Count"].head(hed), label = counts2["UserName"].head(hed), alpha=.6, text_kwargs={'fontsize':fsize})
    if var == 1:
        counts2 = counts[1].copy()
        counts2["Device"] = np.where(counts2["Count"].between(0,counts2["Count"][3000]),"",counts2["Device"])
        squarify.plot(sizes = counts[1]["Count"].head(hed), label = counts2["Device"].head(hed), alpha=.6, text_kwargs={'fontsize':fsize})
    if var == 2:
        counts2 = counts[2].copy()
        counts2["ProcessName"] = np.where(counts2["Count"].between(0,counts2["Count"][250]),"",counts2["ProcessName"])
        squarify.plot(sizes = counts[2]["Count"].head(hed), label = counts2["ProcessName"].head(hed), alpha=.6, text_kwargs={'fontsize':fsize})
    if var == 3:
        counts2 = counts[3].copy()
        counts2["ParentProcessName"] = np.where(counts2["Count"].between(0,counts2["Count"][150]),"",counts2["ParentProcessName"])
        squarify.plot(sizes = counts[3]["Count"].head(hed), label = counts2["ParentProcessName"].head(hed), alpha=.6, text_kwargs={'fontsize':fsize})
    plt.title(str(var)+" counts relative to each other")
    plt.xticks(ticks = [])
    plt.yticks(ticks = [])
    if len(counts[var]["Count"].head(hed)) == len(counts[var]["Count"]):
        plt.savefig("./plots/square/"+str(counts[var].columns[0])+"_Square_Complete.png")
    else:
        plt.savefig("./plots/square/"+str(counts[var].columns[0])+"_Square_"+str(hed)+".png")
    gen_end()
    
def edge_plot(dfo,sour,targ,ident,fract=1,ignore=1,show=True,col=False):
    """This function creates a network in the networkx package and creates and saves an html plot of the network using pyvis: which can also be specified to be shown within the notebook but this could cause slowdown.
    
    Keyword arguments:
    dfo -- the dataframe to work with.
    sour -- the source nodes for the network \(feature to be used from the dataframe\)
    targ -- the target nodes for the network \(feature to be used from the dataframe\)
    ident -- specifies the name of the plot to be saved, the hed value will also be added afterwards.
    fract -- fraction of dataframe to sample. DEFAULT = 1
    ignore -- don't create a connection for variables that have less than this many connections connection. DEFAULT = 1 
    show -- specify a boolean for if you want the plot to be shown within the notebook. DEFAULT = False
    col -- show node and edge colour settings. DEFAULT = False
    """
    dtn()
    G = nx.from_pandas_edgelist(dfo.sample(frac=fract),source=sour,target=targ)
    for component in list(nx.connected_components(G)):
        if len(component)<ignore+2:
            for node in component:
                G.remove_node(node)
    net = Network(height='1000px',width="1600px",notebook=False)
    net.from_nx(G)
    if len(dfo) >= 5000:
        net.toggle_physics(False)
    else:
        net.toggle_physics(True)
    string = "./plots/netx_graphs/plot_"+str(ident)+"_"+str(int(fract*100))+"_percent.html"
    net.barnes_hut(spring_length=320,spring_strength=0.01, overlap=0)
    if col == True:
        net.show_buttons(filter_=["physics","nodes", "edges"])
    else:
        net.show_buttons(filter_=["physics"])
    finish = net.show(string)
    gen_end()
    if show == True:
        return finish
    
