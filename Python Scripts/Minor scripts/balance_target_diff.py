import pandas as pd

D = {}
with open('AUC_4_balanced.json', 'r') as main_file:
    df1 = pd.read_csv(main_file, delim_whitespace = True, lineterminator = '\n', header = None)
    with open('AUC_2_.json', 'r') as comp_file1:
        df2 = pd.read_csv(comp_file1, delim_whitespace = True, lineterminator = '\n', header = None)
        for i in range(0, df2.shape[0]):
            for j in range(0, df1.shape[0]):
                if df2.iloc[i,0] == df1.iloc[j,0]:
                    D[df2.iloc[i,0]] = df2.iloc[i,1]
        with open('AUC_2_balanced.json', 'w') as outpfile:
            for key,value in D.items():
                outpfile.write(key + '\t' + str(value) + '\n')