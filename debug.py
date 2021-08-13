import pandas as pd
import numpy as np

COLUMN_NAMES = ['SUBCHUNK', 'ELASPIC_URL', 'NUM_CORR_INPUT_MUTS',
                'INVALID_SYNTAX', 'NUM_INVALID_SYNTAX',
                'UNRECOG_GENE_SYMBOLS', 'NUM_UNRECOG_GENE_SYMBOLS',
                'UNRECOG_PROT_RESIDUES', 'NUM_UNRECOG_PROT_RESIDUES',
                'DUPLICATES', 'NUM_DUPLICATES',
                'OUTSIDE_STRUCT_DOMAIN', 'NUM_OUTSIDE_STRUCT_DOMAIN',
                'NUM_ACTUAL_INPUT', 'NUM_PROVIDED_INPUT']

data = pd.DataFrame(np.random.randn(5, 14), columns=COLUMN_NAMES[1:])
data[COLUMN_NAMES[0]] = [f'subchunk_{e}' for e in range(1, 6)]
data = data[COLUMN_NAMES]
print(data)
print('***********************************')
print(data['ELASPIC_URL'])
