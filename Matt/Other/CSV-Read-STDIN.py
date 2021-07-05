import csv
import sys
import gzip
from datetime import datetime
import os


with open(sys.argv[1], newline='') as f:

    list_filter = []

    start = datetime.now()

    reader = csv.reader(f)
    ln = next(reader)


    while ln[0] != '':

        print(ln)
        try:
            ln = next(reader)

        except StopIteration:
            break

end = datetime.now()
print('Time Taken: {}'.format(end-start))

# with print statements Time Taken: 1:22:11.862191
# without print statements Time Taken: 0:05:25.499798
# with if statements Time Taken: 0:06:00.598084
# with if statemebt and list appending Time Taken: 0:05:46.897803
