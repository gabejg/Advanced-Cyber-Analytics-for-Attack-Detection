import csv
import sys
import gzip
from datetime import datetime
import os
import numpy as np
import scipy.stats as stats

class StreamingMeanVar:
    def __init__(self):
        self.mean = 0
        self.sum = 0
        self.sumsq = 0
        self.var = 0
        self.n = 0

    def update(self, element):
        self.sum += int(element)
        self.sumsq += int(element) * int(element)
        self.n += 1
        self.mean = self.sum / self.n
        self.var = (self.sumsq / self.n) - self.mean * self.mean

def t_test(mean, var, n, test_mean, test_var, test_n):
    # we implement welch's test here since we have different variances
    test_stat = (test_mean - mean)/(np.sqrt((test_var/test_n)+(var/n)))
    df = ((test_var/test_n + var/n)**2)/((test_var/test_n)**2/(test_n-1)+(var/n)**2/(n-1))
    p_val = stats.t.pdf(test_stat,df)
    return p_val



with open(sys.argv[1], newline='') as f:

    start = datetime.now()

    reader = csv.reader(f)

    ln = next(reader)
    prev_ln = next(reader)
    ln = next(reader)

    i = 0

    vals_b1 = [0,0,0,0,0,0,0,0,0,0,0]

    anomalies = []
    crit_val = 0.0001

    while ln[0]  != '':

        st_idx = int(ln[0]) + 15

        s_dur = StreamingMeanVar()
        s_sp = StreamingMeanVar()
        s_dp = StreamingMeanVar()
        s_sb = StreamingMeanVar()
        s_db = StreamingMeanVar()

        while int(ln[0]) <= st_idx:

            s_dur.update(ln[1])
            s_sp.update(ln[7])
            s_dp.update(ln[8])
            s_sb.update(ln[9])
            s_db.update(ln[10])

            try:
                prev_ln = ln
                ln = next(reader)
            except StopIteration:
                break

        prev_ln[0] = ln[0]

        if i % 2 == 0:
            vals_b1 = [s_dur.mean, s_dur.var, s_sp.mean, s_sp.var, s_dp.mean, s_dp.var, s_sb.mean, s_sb.var, s_db.mean, s_db.var, s_db.n]
            if i == 0:
                pass
            else:
                p_vals = []
                for j in [0,2,4,6,8]:
                    p_val = t_test(vals_b1[j], vals_b1[j+1], vals_b1[10], vals_b2[j], vals_b2[j+1], vals_b2[10])
                    p_vals.append(p_val)
                f_pval = stats.combine_pvalues(p_vals)

                if f_pval[1] <= crit_val:
                    anomalies.append((i,f_pval[1]))
        else:
            vals_b2 = [s_dur.mean, s_dur.var, s_sp.mean, s_sp.var, s_dp.mean, s_dp.var, s_sb.mean, s_sb.var, s_db.mean, s_db.var, s_db.n]
            p_vals = []
            for j in [0,2,4,6,8]:
                p_val = t_test(vals_b1[j], vals_b1[j+1], vals_b1[10], vals_b2[j], vals_b2[j+1], vals_b2[10])
                p_vals.append(p_val)
            f_pval = stats.combine_pvalues(p_vals)

            if f_pval[1] <= crit_val:
                anomalies.append((i,f_pval[1]))

        i += 1

        if i % 1000 == 0:
            print(anomalies)
            print('Time taken for {} blocks: {}. Anomalous instances detected: {}'. format(i, datetime.now()-start, len(anomalies)))

end = datetime.now()
print('Time Taken: {}'.format(end-start))

# with print statements Time Taken: 1:22:11.862191
# without print statements Time Taken: 0:05:25.499798
# with if statements Time Taken: 0:06:00.598084
# with if statemebt and list appending Time Taken: 0:05:46.897803

# netflow - each timestamp corresponds to a single minute

# attempts ended up being fruitless, we get 1/4-1/3 of the chunks detected as anomalies at the 0.0001 level when working with either 1 minute or 15 minute chunks
