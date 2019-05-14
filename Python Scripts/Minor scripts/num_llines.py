import glob
import pandas as pd
import json

D = {}
for file in glob.glob('*.json'):
    df = pd.read_csv(file, delim_whitespace = True, lineterminator = '\n', header = 0)
    D[file] = df.shape[0]

with open('Line of all the files.txt', 'w') as f:
    for k, v in sorted(D.items(), key = lambda x: x[1]):
        f.write(str(k) + ' >>> ' + str(v) + '\n')