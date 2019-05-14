import re
import glob
import pandas as pd

for file in glob.glob('*'):
	with open(file, 'r') as f:
		f = f.readlines()
		for i in f:
			m = re.findall(r'\"Area Under Curve \(AUC\)\"\:(.*)\,\"Mean P0-P1 width', i)
			with open('Liblinear_AUC.json', 'a') as outp:
				for i in m:
					outp.write(file+'\t')
					outp.write(str(i)+'\n')