import pandas as pd
import argparse

parser = argparse.ArgumentParser(description = 'Two files to compare the difference of the number of models between 2 files')
parser.add_argument('--file1', help = 'Check if the elements of this file exist in...')
parser.add_argument('--file2', help = '...this file')
parser.add_argument('--outputfile', help = 'The file that states the difference')
args = parser.parse_args()

D = {}
L = []
with open(args.file2, 'r') as file1:
    df1 = pd.read_csv(file1, delim_whitespace = True, lineterminator = '\n', header = None)
    for i in range(0, df1.shape[0]):
        L.append(df1.iloc[i,0])
    with open(args.file1, 'r') as file2:
        df2 = pd.read_csv(file2, delim_whitespace = True, lineterminator = '\n', header = None)
        for j in range(0, df2.shape[0]):
            if df2.iloc[j,0] not in L:
                D[df2.iloc[j,0]] = df2.iloc[j,1]
                with open(args.outputfile, 'w') as outpfile:
                    for key,value in D.items():
                        outpfile.write(key + '\t' + str(value) + '\n')
