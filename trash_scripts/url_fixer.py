# Looks for each Record and checks if any entry contains default URL.
# which should not be the case. If that entry is recorded, then it must have
# the proper URL which can lead us to 'results' page.

import pandas as pd
from config import ELASPIC_MANY_URL


def url_fixer(tcga, chunk):
    record_path = rf'../Records/{tcga}/record_{tcga}_{chunk}.csv'
    record_data = pd.read_csv(record_path)
    invalid_entries_ix = record_data[record_data['ELASPIC_URL'] == ELASPIC_MANY_URL]['FILE_PATH'].index
    if len(invalid_entries_ix) > 0:
        print(f'Fixing the record_{tcga}_{chunk}.csv ..')
        fixed_data = record_data.drop(invalid_entries_ix, axis='rows').reset_index(drop=True)
        fixed_data.to_csv(rf'../Records/{tcga}/record_{tcga}_{chunk}_fixed.csv', index=False)


def get_bad_urls(tcga, chunk):
    # it doesnt fix it right now.
    record_path = rf'../Records/{tcga}/record_{tcga}_{chunk}.csv'
    record_data = pd.read_csv(record_path)
    data_url_default = record_data[record_data['ELASPIC_URL'] == ELASPIC_MANY_URL]
    if not data_url_default.empty:
        print(record_path)


TCGA = 'OV'
# for c in range(1, 40):
#     url_fixer(TCGA, c)

# url_fixer('OV', 11)

for c in range(1, 40):
    get_bad_urls('OV', c)


# data = pd.read_csv(rf'../Records/OV/record_OV_11.csv')
# invalid_entries_ix = data[data['ELASPIC_URL'] == ELASPIC_MANY_URL]['FILE_PATH'].index
# fixed_data = data.drop(invalid_entries_ix, axis='rows').reset_index(drop=True)
# print(data.shape)
# print(fixed_data.shape)
# assert list(data.index) == list(range(50))
# assert list(fixed_data.index) == list(range(48))
# # fixed_data = data[data['ELASPIC_URL'] == ELASPIC_MANY_URL]
#
# print(data.head())
# print(fixed_data.head())
