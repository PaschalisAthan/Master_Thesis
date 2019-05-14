import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns

L1 = []
L2 = []
L3 = []
L4 = []
with open('AUC_1_balanced.json', 'r') as f1:
    df1 = pd.read_csv(f1, delim_whitespace = True, lineterminator = '\n', header = None)
    for i in range(0, df1.shape[0]):
        L1.append(df1.iloc[i,1])
with open('AUC_2_.json', 'r') as f2:
    df2 = pd.read_csv(f2, delim_whitespace = True, lineterminator = '\n', header = None)
    for i in range(0, df2.shape[0]):
        L2.append(df2.iloc[i,1])
with open('AUC_3_balanced.json', 'r') as f3:
    df3 = pd.read_csv(f3, delim_whitespace = True, lineterminator = '\n', header = None)
    for i in range(0, df3.shape[0]):
        L3.append(df3.iloc[i,1])
with open('AUC_4_.json', 'r') as f4:
    df4 = pd.read_csv(f4, delim_whitespace = True, lineterminator = '\n', header = None)
    for i in range(0, df4.shape[0]):
        L4.append(df4.iloc[i,1])

fig, axes = plt.subplots(2,2, figsize = (4,6), sharey = True)
a = axes[0, 0].violinplot(L1, showmeans = True)
b = axes[1, 0].violinplot(L2, showmeans = True)
c = axes[0, 1].violinplot(L3, showmeans = True)
d = axes[1, 1].violinplot(L4, showmeans = True)
for pc in a['bodies']:
    pc.set_facecolor('y')
    pc.set_edgecolor('y')
    pc.set_alpha(1)
a['cmeans'].set_color('b')
a['cmins'].set_color('y')
a['cmaxes'].set_color('y')
a['cbars'].set_color('y')
for pc in b['bodies']:
    pc.set_facecolor('c')
    pc.set_edgecolor('c')
    pc.set_alpha(1)
b['cmeans'].set_color('r')
b['cmins'].set_color('c')
b['cmaxes'].set_color('c')
b['cbars'].set_color('c')
for pc in c['bodies']:
    pc.set_facecolor('y')
    pc.set_edgecolor('y')
    pc.set_alpha(1)
c['cmeans'].set_color('b')
c['cmins'].set_color('y')
c['cmaxes'].set_color('y')
c['cbars'].set_color('y')
for pc in d['bodies']:
    pc.set_facecolor('c')
    pc.set_edgecolor('c')
    pc.set_alpha(1)
d['cmeans'].set_color('r')
d['cmins'].set_color('c')
d['cmaxes'].set_color('c')
d['cbars'].set_color('c')
plt.setp(axes[0, 0].get_xticklabels(), visible = False)
plt.setp(axes[1, 0].get_xticklabels(), visible = False)
plt.setp(axes[0, 1].get_xticklabels(), visible = False)
plt.setp(axes[1, 1].get_xticklabels(), visible = False)
yellow_patch = mpatches.Patch(color = 'c', label = 'Without Duplicates')
cyan_patch = mpatches.Patch(color = 'y', label = 'With Duplicates')
plt.legend(handles = [cyan_patch, yellow_patch], loc = 'upper center', bbox_to_anchor = (-0.1, -0.1), ncol = 2)
plt.show()
