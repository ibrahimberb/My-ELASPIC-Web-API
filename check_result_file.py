import pandas as pd
import glob
import os

# TODO: Implement later.

for file in glob.glob('test_files/ELASPIC_Results_TEST/OV/*'):
    data = pd.read_table(file, sep='\t')
    filename = os.path.basename(file)
    print('filename: {} | error entries: {}'.format(filename, data['Status'].value_counts()['error']))
