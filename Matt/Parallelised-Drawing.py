import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import gzip
import shutil
import pickle
import datetime

from itertools import product
from multiprocessing import Pool, cpu_count, current_process

import networkx as nx

def draw_day(data,i):

    # split the data into the selected time period
    df_day = data

    # print day we're working on
    print(i)

    # get all unqiue users for that period
    userlist_1 = list(list(df_day[0].unique()))
    userlist_2 = list(list(df_day[1].unique()))
    unique_users = set(userlist_1 + userlist_2)

    # get all connections made for that period
    connections = zip(df_day[0], df_day[1])

    # create the graph
    G = nx.DiGraph()

    # create the nodes of the graph
    for u in unique_users:
        G.add_node(u)

    # create the edges of the graph
    for a in connections:
        G.add_edge(*a)

    # draw the network
    plt.figure(figsize=(15,15), dpi=400)
    nx.draw(G, node_size=20, linewidths=0.8)
    plt.savefig('day {}.png'.format(i))

    return G

# parallelisation
if __name__ == "__main__":

    begin_time = datetime.datetime.now()
    # print the number of cores
    print("Number of cores available equals %s" % cpu_count())
    print("Using %s cores" % '8')


    # importing data
    try:
        authentication_data = pickle.load(open('../Data/Authentication_data.p','rb'))
        process_data = pickle.load(open('../Data/Authentication_data.p','rb'))
    except:

        rootdir = 'C:/Users/corri/OneDrive/Documents/Uni/Postgraduate/Final Project/LANL/ATI Data/Summaries/wls'
        unzippeddir = 'C:/Users/corri/OneDrive/Documents/Uni/Postgraduate/Final Project/LANL/ATI Data/Summaries/wls/Unzipped'
        frames = []

        count = 0

        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                filedir = rootdir + '/' + file
                with gzip.open(filedir) as f:
                    df = pd.read_csv(filedir, header=None)
                    frames.append(df)
                if 'authentications' in str(file):
                    count = count + len(df)

        df = pd.concat(frames)

        authentication_data = df[:count]
        process_data = df[count:]
        pickle.dump(authentication_data, open('../Data/Authentication_data.p','wb'))
        pickle.dump(process_data, open('../Data/Process_data.p','wb'))


    index_list = authentication_data.index.tolist()
    start_days = [i for i, e in enumerate(index_list) if e == 0]
    start_days.append(len(authentication_data))

    data_ = [(authentication_data[start_days[i]:start_days[i+1]],i) for i in range(len(start_days)-1)]

    # multiprocessing
    pool = Pool(processes = 8)

    with pool as p:
        results = p.starmap(draw_day, data)

    print("Finished creating networks!")
    end_time = datetime.datetime.now()
    print(end_time - begin_time)
