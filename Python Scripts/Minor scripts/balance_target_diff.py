import pandas as pd
import argparse

parser = argparse.ArgumentParser(description = 'Two files to compare the difference of the number of models between 2 files')
parser.add_argument('--file1', help = 'If an element of this file does not exist in...')
parser.add_argument('--file2', help = '...this file...')
parser.add_argument('--outputfile', help = '...write it in this file')
args = parser.parse_args()

D = {}
with open(args.files2, 'r') as main_file:
    df1 = pd.read_csv(main_file, delim_whitespace = True, lineterminator = '\n', header = None)
    with open(args.file1, 'r') as comp_file1:
        df2 = pd.read_csv(comp_file1, delim_whitespace = True, lineterminator = '\n', header = None)
        for i in range(0, df2.shape[0]):
            for j in range(0, df1.shape[0]):
                if df2.iloc[i,0] == df1.iloc[j,0]:
                    D[df2.iloc[i,0]] = df2.iloc[i,1]
        with open(args.outputfile, 'w') as outpfile:
            for key,value in D.items():
                outpfile.write(key + '\t' + str(value) + '\n')