# Looks for each Record and checks if any entry contains default URL.
# which should not be the case. If that entry is recorded, then it must have
# the proper URL which can lead us to 'results' page.

import pandas as pd
from config import ELASPIC_MANY_URL


def url_fixer(tcga, chunk):
    # it doesnt fix it right now.

    record_path = rf'../Records/{tcga}/record_{tcga}_{chunk}.csv'

    record_data = pd.read_csv(record_path)

    data_url_default = record_data[record_data['ELASPIC_URL'] == ELASPIC_MANY_URL]
    if not data_url_default.empty:
        print(record_path)


TCGA = 'OV'
for chunk in range(1, 40):
    url_fixer(TCGA, chunk)

# ensurer(25, 1)
