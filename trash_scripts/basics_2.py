# # get number of active computations from each record.
#
# import pandas as pd
# from config import ELASPIC_MANY_URL
#
#
# def get_num_active_computations(tcga, chunk):
#     record_path = rf'../Records/OV/record_{tcga}_{chunk}.csv'
#
#     record_data = pd.read_csv(record_path)
#     num_active_computations = len(record_data[(record_data['UPLOADED_STATUS'] == 1) &
#                                               (record_data['DOWNLOADED_STATUS'] == 0)])
#
#     print(f"TCGA: {TCGA} \t CHUNK: {chunk} \t NUM_ACTIVE_COMPUTATIONS: {num_active_computations}")
#
#
# TCGA = 'OV'
# for chunk in range(1, 40):
#     get_num_active_computations(TCGA, chunk)
#
# # ensurer(25, 1)


L = list(range(1, 128))
exclude = [1, 2, 3, 4]
L = [e for e in L if e not in exclude]
print(L)
