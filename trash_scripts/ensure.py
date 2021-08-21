import os
import pandas as pd
from tqdm import tqdm


def ensurer(chunk, subchunk):
    TEST_INPUT_PATH = f'../ELASPIC_Input/OV/{chunk}/SNV_OV_Chunk_{chunk}_{subchunk}.txt'
    TEST_RESULT_PATH = f'../Elaspic_Results/OV/{chunk}/allresults_OV_{chunk}_{subchunk}.txt'

    with open(TEST_INPUT_PATH) as f:
        lines = f.readlines()

    result_data = pd.read_csv(TEST_RESULT_PATH, sep='\t')

    for _, row in result_data.iloc[:, [1, 2]].iterrows():
        # print((row['UniProt_ID'], row['Mutation']))
        assert row['UniProt_ID'] in str(lines)
        assert row['Mutation'] in str(lines)


for i in tqdm(range(1, 40)):
    for j in range(1, 101):
        try:
            ensurer(i, j)
        except FileNotFoundError:
            pass



# ensurer(25, 1)