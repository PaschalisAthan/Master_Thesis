import pandas as pd
import argparse
import random

parser = argparse.ArgumentParser(description = 'Predicting Target Profile')
parser.add_argument('--in_file', help = 'The file with the molecules to predict')
parser.add_argument('--outp_smiles', help = 'The file with only the canonical SMILES')

args = parser.parse_args()
with open(args.in_file, 'r') as inpfile:
	df = pd.read_csv(inpfile, delimiter = ';', lineterminator = '\n', header = 0)
	l = []

	for i in range(0, df.shape[0]):
		l.append(df.iloc[i, 2])

	with open(args.outp_smiles + '_smiles.tsv', 'w') as outfile:
		outfile.write('SMILES' + '\t' + 'FLAG' + '\n')
		for i in l:
			outfile.write(i + '\t' + str(0) + '\n')
