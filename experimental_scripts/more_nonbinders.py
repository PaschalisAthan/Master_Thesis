import argparse
import pandas as pd
import sys, csv, operator, os
import random

#ls -1a *[!x]json
parser = argparse.ArgumentParser(description = 'Balance files with many nonbinders')
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename, 'r') as file:
    L0 = []
    L1 = []
    df = pd.read_csv(file, delim_whitespace = True, lineterminator = '\n', header = 0)
    zero_counter = 0
    one_counter = 0
    for i in range(0, df.shape[0]):
        if int(df.iloc[i,1]) == 0:
            zero_counter += 1
        elif int(df.iloc[i,1]) == 1:
            one_counter += 1
    dif = one_counter - zero_counter
    if dif < 0:
        if one_counter == 0:
            os.rename('./' + args.filename, './only_non_binders/' + args.filename)
        else:
            nonbinders = one_counter
            df2 = pd.read_csv(file, delim_whitespace = True, lineterminator = '\n', header = 0)
            for j in range(0, df2.shape[0]):
                if df2.iloc[j,1] == 1:
                    L1.append(df2.iloc[j,0])
                    L1.append('\t')
                    L1.append(df2.iloc[j,1])
                    L1.append('\n')
            while nonbinders > 0:
                k = random.randint(0, df2.shape[0]-1)
                if df2.iloc[k,1] == 0:
                    L0.append(df2.iloc[k,0])
                    L0.append('\t')
                    L0.append(df2.iloc[k,1])
                    L0.append('\n')
                    nonbinders -= 1
            with open(file, 'r') as inp, open(file, 'w') as outp:
                outp.write('SMILES' + '\t' + 'FLAG' + '\n')
                for m in L0:
                    outp.write(str(m))
                for n in L1:
                    outp.write(str(n))
    
