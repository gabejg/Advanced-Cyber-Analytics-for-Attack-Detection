#!/usr/bin/env python
# coding: utf-8

# # Process Data

# The intention in this notebook is to look into the process data. We'll perform some EDA such as Data Cleaning, Seperation and Outlier Detection and then start running some anomaly detection models on the data.

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import gzip
import shutil
import datetime
import networkx as nx

from IPython.display import clear_output


# ### Data

# First we import our data. We import both process and authentication data incase the latter becomes useful down the line.

# In[2]:


try:
    print('Attempting to read entire data set.')
    authentication_data = pd.read_csv('Authentication data.gz', compression='gzip', index_col = 0)
    process_data = pd.read_csv('Process data.gz', compression='gzip', index_col = 0)
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


# In[3]:


rows = process_data.shape[0]
features = process_data.shape[1]
dp = process_data.shape[0] * process_data.shape[1]

print('The process data contains {} rows with {} features each. Thus we have {} data points.'.format(rows, features, dp))


# In[4]:


process_data.head()


# ### EDA

# In[5]:


process_data.groupby('UserName').size().sort_values(ascending=False)


# In[6]:


process_data.groupby('Device').size().sort_values(ascending=False)


# In[7]:


process_data.groupby('ProcessName').size().sort_values(ascending=False)


# In[8]:


process_data.groupby('ParentProcessName').size().sort_values(ascending=False)


# We're going to find the index's to seperate out the days. Due to the way we created the large data set, we can search for the index 0 which tells us the start of every day.

# In[9]:


index_list = process_data.index.tolist()
start_days = [i for i, e in enumerate(index_list) if e == 0]
start_days.append(len(process_data))


# Lets now seperate out day 1 and understand what we can do with the data.

# In[10]:


process_day_1 = process_data[start_days[0]:start_days[1]]
process_day_1


# ### Dummy Variables

# We'll create a quick and dirty dummy variable creation function. We could use the get_dummies function from pandas but this creates rows instead of doing it inplace which would result in a massive amount of features which would essentially be unhandleable when working with the entire data set.

# In[11]:


def dummy(row, data):
    row_vals = data[row].unique()
    row_vals_dict = {}
    for i, key in enumerate(row_vals):
        row_vals_dict[key] = i

    return row_vals_dict


# In[12]:


user_names_dict = dummy('UserName', process_day_1)
devices_dict = dummy('Device', process_day_1)
processes_dict = dummy('ProcessName', process_day_1)
parent_processes_dict = dummy('ParentProcessName', process_day_1)

dummy_process_day_1 = pd.DataFrame()

dummy_process_day_1['UserName'] = process_day_1['UserName'].map(user_names_dict)
dummy_process_day_1['Device'] = process_day_1['Device'].map(devices_dict)
dummy_process_day_1['ProcessName'] = process_day_1['ProcessName'].map(processes_dict)
dummy_process_day_1['ParentProcessName'] = process_day_1['ParentProcessName'].map(parent_processes_dict)
dummy_process_day_1['DailyCount'] = process_day_1['DailyCount']


# In[13]:


dummy_process_day_1


# So we've converted our object variables into integers successfully!

# ### Clustering

# We'll attempt to run a DBSCAN clustering on this data set now. This will give us a good indication of whether the data set is useful for anomaly detection or not since DBSCAN is effective at picking up anomalous data from unlabelled data. The below is a snippet of the grid search we perform on the HPC which we will later import.

# We'll analyse the effectiveness of our parameters through the number of clusters produced, the number of noise points and the silhouette score.

# The silhouette score is defined when the number of labels i.e. clusters produced is $ 2 < clusters < samples - 1 $. It takes values in $ [-1,1] $ with -1 being the worst score and 1 being the best score.

# In[14]:


from sklearn.cluster import DBSCAN
from sklearn import metrics


# In[15]:


eps = [1,2,5,10,25,50,100,200]

min_samples = [100,50,25,15,10]

no_clust = []
no_noise = []
sil_score = []
e_m = []

for e in eps:
    for ms in min_samples:

        clear_output(wait=True)
        print('Working with eps = {} and min_samples = {}'.format(e,ms))

        e_m.append((e,ms))

        db = DBSCAN(eps=e, min_samples=ms).fit(dummy_process_day_1)
        labels = db.labels_
        no_clust.append(len(np.unique(labels)))
        no_noise.append(np.sum(np.array(labels) == -1, axis=0))

        if len(np.unique(labels)) == 1:
            sil_score.append(0)
        else:
            sil_score.append(metrics.silhouette_score(dummy_process_day_1, labels))


# From reference [2] from our bibliography, we would expect min_samples=10 to give us our best results since $ 2 * dim = 10 $, however the data set is likely to contain a lot of noise and is a large data set so this may need to be increased. As for $ \epsilon $, we will use methods such as the elbow method, largest cluster size and noise % to determine this. Silhouette score will also give us a good indicator.

# In[22]:


DBSCAN_parameter_search = pd.DataFrame()

DBSCAN_parameter_search['no_clusters'] = no_clust
DBSCAN_parameter_search['no_noise'] = no_noise
DBSCAN_parameter_search['Silhoutte Score'] = sil_score
DBSCAN_parameter_search.index = e_m
DBSCAN_parameter_search.to_csv('Grid Search HPC.csv',header=True)


# In[21]:


DBSCAN_parameter_search


# In[ ]:
