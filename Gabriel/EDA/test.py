import modin.pandas as pd
from datetime import datetime as dt
from distributed import Client

client = Client()

start = dt.now()
df = pd.read_csv("https://www.dropbox.com/s/c065rcq72abzm0s/Authentication_data.gz?dl=1",compression="gzip")
print("completed in: "+str(dt.now()-start))
