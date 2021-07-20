from pyCP_APR import CP_APR

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import os.path
import gzip
import shutil
import datetime
import networkx as nx
import pickle
from scipy import stats
from scipy import sparse
import bz2
import random
random.seed(1134)

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor

from IPython.display import clear_output
from multiprocessing import Pool, cpu_count, current_process
import sys

# creating the function to get title, articles and tags

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

def auth_type_un_df(user,authentication_data,n=24):
    auth_type_df = pd.DataFrame(index = list(authentication_data['Authent Type'].unique()))
    n = n
    auth_type_dict = {}
    auth_index_list = authentication_data.index.tolist()
    auth_start_days = [i for i, e in enumerate(auth_index_list) if e == 0]
    auth_start_days.append(len(authentication_data))

    for i in range(len(auth_start_days)-1):
        chunks = split_dataframe(authentication_data[auth_start_days[i]:auth_start_days[i+1]],n)
        for j in range(n):
                data = chunks[j]
                auth_type_data = data[data['UserName'] == user].groupby('Authent Type').size()
                auth_type_dict[i*n + j] = auth_type_df.index.to_series().map(auth_type_data.to_dict())

    auth_type_df = pd.DataFrame(data=auth_type_dict,index = list(authentication_data['Authent Type'].unique()))
    auth_type_df = auth_type_df.transpose()
    auth_type_df = auth_type_df.fillna(0)

    return auth_type_df

def scaled_iso_lof(user,authentication_data,plot=False,c='auto'):

    data = auth_type_un_df(user,authentication_data)

    # scaling
    scaler = StandardScaler()
    scaled_data = pd.DataFrame(scaler.fit_transform(data))

    # isolation forest predictions
    if_model = IsolationForest(contamination=c)
    if_predictions = if_model.fit_predict(data)

    # local outlier factor predictions
    lof = LocalOutlierFactor(n_neighbors=2)
    lof_predictions = lof.fit_predict(data)

    if plot == True:

        # PCA reduction for plotting
        pca = PCA(n_components=2)
        auth_types_pca = pd.DataFrame(pca.fit_transform(data))

        # finding anomaly locations
        a_if = auth_types_pca.loc[if_predictions == -1]
        a_lof = auth_types_pca.loc[lof_predictions == -1]

        anomalies = auth_types_pca.loc[list(set(a_lof.index) & set(a_if.index))]

        fig, ax = plt.subplots(figsize=(20,6))
        ax.plot(auth_types_pca[0], auth_types_pca[1], color='black', label='Normal')
        ax.scatter(anomalies[0], anomalies[1], color='red', label='Anomaly')
        ax.set_xlabel("Time")
        ax.set_ylabel("Number of Events")
        ax.text(0,auth_types_pca[1].max()-0.1,('Number of combined anomalies found: {}. \n Number of LOF anomalies found: {}. \n Number of IF anomalies found: {}.'.format(len(anomalies), len(a_lof), len(a_if))))
        plt.legend(loc=1)

    else:
        a_if = data.loc[if_predictions == -1]
        a_lof = data.loc[lof_predictions == -1]

        anomalies = data.loc[list(set(a_lof.index) & set(a_if.index))]

        score = 1-(len(anomalies)/len(data))

    return score,user


# creating our multi-processing

if __name__ == "__main__":

    s_main = datetime.datetime.now()

    # print the number of cores
    print("Number of cores available equals %s" % cpu_count())
    print("Using %s cores" % 8)

    try:
        print('Attempting to read entire data set.')
        authentication_data = pd.read_csv('../Data/Authentication data.gz', compression='gzip', index_col = 0)
        process_data = pd.read_csv('../Data/Process data.gz', compression='gzip', index_col = 0)
    except:
        clear_output()
        print('Unable to read entire data set, reading from original files.')
        rootdir = 'C:/Users/corri/OneDrive/Documents/Uni/Postgraduate/Final Project/LANL/ATI Data/Summaries/wls'
        unzippeddir = 'C:/Users/corri/OneDrive/Documents/Uni/Postgraduate/Final Project/LANL/ATI Data/Summaries/wls/Unzipped'
        frames = []

        count = 0

        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file[-3:] == '.gz':
                    filedir = rootdir + '/' + file
                    with gzip.open(filedir) as f:
                        df = pd.read_csv(filedir, header=None)
                        frames.append(df)
                    if 'authentications' in str(file):
                        count = count + len(df)

        df = pd.concat(frames)

        authentication_data = df[:count]
        authentication_data.columns = ['UserName', 'SrcDevice','DstDevice', 'Authent Type', 'Failure', 'DailyCount']

        process_data = df[count:]
        process_data = process_data[[0,1,2,3,4]]
        process_data.columns = ['UserName', 'Device', 'ProcessName', 'ParentProcessName', 'DailyCount']

        authentication_data.to_csv('../Data/Authentication data.gz', header=True, compression='gzip')
        process_data.to_csv('../Data/Process data.gz', header=True, compression='gzip')

    train_users = list(authentication_data['UserName'].unique())
    test_users = list(authentication_data['UserName'].unique())

    a_t = list(authentication_data['Authent Type'].unique())
    AT_dict = { i : a_t[i] for i in range(0, len(a_t))}

    auth_index_list = authentication_data.index.tolist()
    auth_start_days = [i for i, e in enumerate(auth_index_list) if e == 0]
    auth_start_days.append(len(authentication_data))

    e_main = datetime.datetime.now()
    print('Time taken to complete data reading & production: {}.'.format(e_main-s_main))
    # create a pool of workers
    # start all worker processes
    pool = Pool(processes = 8)

    mp_list = [[un,authentication_data] for un in train_users[:int(sys.argv[1])]]

    begin_time = datetime.datetime.now()

    # context manager so no need to close
    with pool as p:
        results = p.starmap(scaled_iso_lof, mp_list)

    end_time = datetime.datetime.now()
    print("Finished getting all dataframes in {}.".format(end_time - begin_time))
