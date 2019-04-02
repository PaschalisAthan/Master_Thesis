import sys, csv, operator, os
import pandas as pd
import glob
import random
import argparse

parser = argparse.ArgumentParser(description = 'Balance files with many binders')
parser.add_argument('filename')
args = parser.parse_args()

df1 = pd.read_csv('output', delimiter = '\t', lineterminator = '\n', header = 0 )
with open(args.filename, 'r') as file:
    df2 = pd.read_csv(file, delim_whitespace = True, lineterminator = '\n', header = 0)
    L1 = list(df2.iloc[:,0])
    zero_counter = 0
    one_counter = 0
    for i in range(0, df2.shape[0]):
        if int(df2.iloc[i,1]) == 0:
            zero_counter += 1
        elif int(df2.iloc[i,1]) == 1:
            one_counter += 1
    dif = one_counter - zero_counter
    while dif > 0:
        z = random.randint(0,df1.shape[0]-1)
        if df1.iloc[z,1] not in L1:
            if df1.iloc[z,2] == 'IC50' and df1.iloc[z,3]>10000:
                dif += -1
                with open(args.filename, 'a') as f2:
                    f2.write(df1.iloc[z,1])
                    f2.write('\t')
                    f2.write(str(0))
                    f2.write('\n')
            elif df1.iloc[z,2] == 'Ki' and df1.iloc[z,3]>5000:
                dif += -1
                with open(args.filename, 'a') as f2:
                    f2.write(df1.iloc[z,1])
                    f2.write('\t')
                    f2.write(str(0))
                    f2.write('\n')
            elif df1.iloc[z,2] == 'Kd' and df1.iloc[z,3]>5000:
                dif += -1
                with open(args.filename, 'a') as f2:
                    f2.write(df1.iloc[z,1])
                    f2.write('\t')
                    f2.write(str(0))
                    f2.write('\n')
            elif df1.iloc[z,2] == 'EC50' and df1.iloc[z,3]>10000:
                dif += -1
                with open(args.filename, 'a') as f2:
                    f2.write(df1.iloc[z,1])
                    f2.write('\t')
                    f2.write(str(0))
                    f2.write('\n')
