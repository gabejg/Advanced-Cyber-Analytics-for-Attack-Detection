def process_import():
    try:
        print("Looking for local copy of Process data...")
        dtn()
        df_p = pd.read_csv("G:/Users/Gabriel/Documents/Education/UoB/GitHubDesktop/Advanced-Cyber-Analytics-for-Attack-Detection/Data/Process data.gz",compression="gzip",index_col=0)
        stop = end()
        print("Process data fetched locally in "+stop)
        return df_p
    except OSError as e:
        if e.errno == 2:
            print("No Local Process data found. Importing from the web.")
            dtn()
            df_p = pd.read_csv("https://www.dropbox.com/s/c065rcq72abzm0s/Process_data.gz?dl=1",compression="gzip")
            stop = end()
            print("Process data fetched from web in "+stop)
            return df_p
        else:
            print(e)

def auth_import():
    try:
        print("Looking for local copy of Auth data...")
        dtn()
        df_a = pd.read_csv("G:/Users/Gabriel/Documents/Education/UoB/GitHubDesktop/Advanced-Cyber-Analytics-for-Attack-Detection/Data/Authentication data.gz",compression="gzip",index_col=0)
        stop = end()
        print("Auth data fetched locally in "+stop)
        return df_a
    except OSError as e:
        if e.errno == 2:
            print("No Local Auth data found. Importing from the web.")
            dtn()
            df_a = pd.read_csv("https://www.dropbox.com/s/c065rcq72abzm0s/Authentication_data.gz?dl=1",compression="gzip")
            stop = end()
            print("Auth data fetched from web in "+stop)
            return df_a
        else:
            print(e)
    