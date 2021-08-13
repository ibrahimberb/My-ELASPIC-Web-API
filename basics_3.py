import pandas as pd

data = pd.read_csv('Records_Test/record_BRCA_22.csv', index_col='SUBCHUNK')
print(data)
