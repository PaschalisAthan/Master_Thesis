import sys, csv, operator, os
import pandas as pd
import glob
import random
import argparse

parser = argparse.ArgumentParser(description = 'Balance files with many binders')
parser.add_argument('filename')
parser.add_argument('output_folder')
args = parser.parse_args()

df_0 = pd.read_csv('database', delimiter = '\t', lineterminator = '\n', header = 0 )
os.chdir(args.output_folder)
with open(args.filename, 'r') as file:
    L0 = []
    L1 = []
    df_1 = pd.read_csv(file, delim_whitespace = True, lineterminator = '\n', header = 0)
    L_nb = list(df_1.iloc[:,0])
    zero_counter = 0
    one_counter = 0
    for i in range(0, df_1.shape[0]):
        if int(df_1.iloc[i,1]) == 0:
            zero_counter += 1
        elif int(df_1.iloc[i,1]) == 1:
            one_counter += 1
    dif = one_counter - zero_counter
    if dif < 0:
        if one_counter == 0:
            os.rename('./' + args.filename, './only_non_binders/' + args.filename)
        else:
            nonbinders = one_counter
            for j in range(0, df_1.shape[0]):
                if df_1.iloc[j,1] == 1:
                    L1.append(df_1.iloc[j,0])
                    L1.append('\t')
                    L1.append(df_1.iloc[j,1])
                    L1.append('\n')
            while nonbinders > 0:
                k = random.randint(0, df_1.shape[0]-1)
                if df_1.iloc[k,1] == 0:
                    L0.append(df_1.iloc[k,0])
                    L0.append('\t')
                    L0.append(df_1.iloc[k,1])
                    L0.append('\n')
                    nonbinders -= 1
            with open(args.filename.replace('.json', '') + '_balanced.json', 'w') as outp:
                outp.write('SMILES' + '\t' + 'FLAG' + '\n')
                for m in L0:
                    outp.write(str(m))
                for n in L1:
                    outp.write(str(n))        
    elif dif >0:
        with open(args.filename.replace('.json', '') + '_balanced.json', 'w') as f:
            f.write('SMILES')
            f.write('\t')
            f.write('FLAG')
            f.write('\n')
            for k in range(0, df_1.shape[0]):
                f.write(df_1.iloc[k,0])
                f.write('\t')
                f.write(str(df_1.iloc[k,1]))
                f.write('\n')
        while dif > 0:
            z = random.randint(0,df_0.shape[0]-1)
            if df_0.iloc[z,1] not in L_nb:
                if df_0.iloc[z,2] == 'IC50' and df_0.iloc[z,3]>10000:
                    dif += -1
                    with open(args.filename.replace('.json', '') + '_balanced.json', 'a') as f:
                        f.write(df_0.iloc[z,1])
                        f.write('\t')
                        f.write(str(0))
                        f.write('\n')
                elif df_0.iloc[z,2] == 'Ki' and df_0.iloc[z,3]>5000:
                    dif += -1
                    with open(args.filename.replace('.json', '') + '_balanced.json', 'a') as f:
                        f.write(df_0.iloc[z,1])
                        f.write('\t')
                        f.write(str(0))
                        f.write('\n')
                elif df_0.iloc[z,2] == 'Kd' and df_0.iloc[z,3]>5000:
                    dif += -1
                    with open(args.filename.replace('.json', '') + '_balanced.json', 'a') as f:
                        f.write(df_0.iloc[z,1])
                        f.write('\t')
                        f.write(str(0))
                        f.write('\n')
                elif df_0.iloc[z,2] == 'EC50' and df_0.iloc[z,3]>10000:
                    dif += -1
                    with open(args.filename.replace('.json', '') + '_balanced.json', 'a') as f:
                        f.write(df_0.iloc[z,1])
                        f.write('\t')
                        f.write(str(0))
                        f.write('\n')


