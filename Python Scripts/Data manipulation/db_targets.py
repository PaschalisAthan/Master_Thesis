import argparse
import pandas as pd
import os

#"--input", type = file, help = "input filename"
parser = argparse.ArgumentParser(description = 'Process the Chembl database')
parser.add_argument('--database', help = 'The database to take the targets from')
parser.add_argument('--outdir', help = 'The folder to produce the target files')

args = parser.parse_args()
with open(args.database, 'r') as dbfile:
    df = pd.read_csv(dbfile, delimiter = '\t', lineterminator = '\n', header = 0)
    D={}

    for i in range(0, df.shape[0]):
        df.iloc[i, 0] = df.iloc[i, 0].replace('/','-')
        df.iloc[i, 0] = df.iloc[i, 0].replace(' ','_')
        df.iloc[i, 0] = df.iloc[i, 0].replace('(','_')
        df.iloc[i, 0] = df.iloc[i, 0].replace(')','_')
        df.iloc[i, 0] = df.iloc[i, 0].replace("'",'')
        df.iloc[i, 0] = df.iloc[i, 0].replace(">",'')

    for i in range(0, df.shape[0]):
        if df.iloc[i, 0] not in D:
            D[df.iloc[i, 0]] = []

    for j in range(0, df.shape[0]):
        D.setdefault(df.iloc[j,0],[]).append(df.iloc[j,1]+'\t')
        if df.iloc[j,2]=='IC50' and df.iloc[j,3]>10000:
            D.setdefault(df.iloc[j,0],[]).append('0\n')
        elif df.iloc[j,2]=='IC50' and df.iloc[j,3]<=10000:
            D.setdefault(df.iloc[j,0],[]).append('1\n')
        elif df.iloc[j,2]=='Ki' and df.iloc[j,3]>5000:
            D.setdefault(df.iloc[j,0],[]).append('0\n')
        elif df.iloc[j,2]=='Ki' and df.iloc[j,3]<=5000:
            D.setdefault(df.iloc[j,0],[]).append('1\n')
        elif df.iloc[j,2]=='Kd' and df.iloc[j,3]>5000:
            D.setdefault(df.iloc[j,0],[]).append('0\n')
        elif df.iloc[j,2]=='Kd' and df.iloc[j,3]<=5000:
            D.setdefault(df.iloc[j,0],[]).append('1\n')
        elif df.iloc[j,2]=='EC50' and df.iloc[j,3]>10000:
            D.setdefault(df.iloc[j,0],[]).append('0\n')
        elif df.iloc[j,2]=='EC50' and df.iloc[j,3]<=10000:
            D.setdefault(df.iloc[j,0],[]).append('1\n')

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    for key,value in D.items():
        with open(os.path.join(args.outdir, key + '.tsv'), 'w+') as outfile:
            outfile.write('SMILES' + '\t' + 'FLAG' + '\n')
            outfile.write(''.join(value))
