import pandas as pd

data = pd.read_table('allresults.txt', sep='\t')
print(data.shape)
print(data.iloc[:, [1, 2, 4, 19, 30]].head())