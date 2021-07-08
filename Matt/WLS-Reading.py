import csv
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import datetime
import bz2
import sys
import networkx as nx

from IPython.display import clear_output

def WLS_reader(day):

    json_data_no_proc = []

    s_time = datetime.datetime.now()

    with bz2.open('C:\\Users\\corri\\Downloads\\wls_day-' + str(day) + '.bz2',"rt") as f:
        for line in f:
            ln = json.loads(line)
            if ('LogonType' in ln.keys()) and ('ProcessName' not in ln.keys()):
                json_data_no_proc.append(ln)
            else:
                pass

    wls_auths_no_proc = pd.DataFrame(json_data_no_proc)

    e_time = datetime.datetime.now()

    print('Reading data took: {}.'.format(e_time - s_time))

    print('{} lines read.'.format(wls_auths_no_proc.shape[0]))

    return wls_auths_no_proc

def split_dataframe(df,n):
    chunks = list()
    chunk_size = int(np.round(df.shape[0]/n))
    num_chunks = n
    for i in range(num_chunks):
        if i != num_chunks-1:
            chunks.append(df[i*chunk_size:(i+1)*chunk_size])
        else:
            chunks.append(df[i*chunk_size:])
    return chunks

def degree_splits(data,n):

    UserNames = list(data['UserName'].unique())
    degree_sets = pd.DataFrame(index=UserNames)

    chunks = split_dataframe(data,n)

    if len(chunks) != n:
        print('ERROR: Number of chunks is not {}.'.format(n))

    for j in range(n):
        clear_output(wait=True)
        print('Working with section {} of {}.'.format(j+1,n))
        data = chunks[j]
        # create graph
        auth_set_G = nx.from_pandas_edgelist(data,source="UserName",target="LogHost")
        # create degree dictionary
        dict_degrees = {n:d for n,d in auth_set_G.degree()}
        # map dictionary to data frame()
        degree_sets[j] = degree_sets.index.to_series().map(dict_degrees)

    degree_sets = degree_sets.fillna(0)
    degree_sets = degree_sets.transpose()

    return degree_sets

day_auths_file = WLS_reader(sys.argv[1])
day_degrees = degree_splits(day_auths_file,8)
day_degrees.to_csv('Day {} degrees.csv'.format(sys.argv[1]))
