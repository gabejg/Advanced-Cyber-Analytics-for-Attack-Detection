import pandas as pd
import numpy as np
from IPython.display import clear_output

from scipy import sparse
from multiprocessing import Pool, cpu_count, current_process
import datetime
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

def auth_type_un_df(user,n,authentication_data):
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

def sparse_df(username,authentication_data,n=24):

    df = auth_type_un_df(username,n,authentication_data)

    s = sparse.coo_matrix(df)
    co = [[s.row[i],s.col[i],1] for i in range(len(s.row))]
    vals = s.data

    return vals, co


# creating our multi-processing

if __name__ == "__main__":

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

    # create a pool of workers
    # start all worker processes
    pool = Pool(processes = 8)

    mp_list = [[un,authentication_data] for un in train_users[:int(sys.argv[1])]]

    begin_time = datetime.datetime.now()

    # context manager so no need to close
    with pool as p:
        results = p.starmap(sparse_df, mp_list)

    end_time = datetime.datetime.now()
    print("Finished getting {} dataframes in {}.".format(sys.argv[1], end_time - begin_time))
