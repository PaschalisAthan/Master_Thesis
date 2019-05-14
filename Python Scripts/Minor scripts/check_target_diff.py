import pandas as pd

D = {}
L = []
with open('AUC_4_.json', 'r') as file1:
    df1 = pd.read_csv(file1, delim_whitespace = True, lineterminator = '\n', header = None)
    for i in range(0, df1.shape[0]):
        L.append(df1.iloc[i,0])
    with open('AUC_2_.json', 'r') as file2:
        df2 = pd.read_csv(file2, delim_whitespace = True, lineterminator = '\n', header = None)
        for j in range(0, df2.shape[0]):
            if df2.iloc[j,0] not in L:
                D[df2.iloc[j,0]] = df2.iloc[j,1]
                with open('4_2_difference.json', 'w') as outpfile:
                    for key,value in D.items():
                        outpfile.write(key + '\t' + str(value) + '\n')
