# August 16, 2021

from config import (RECORDS_FOLDER_PATH,
                    ELASPIC_RESULTS_FOLDER_PATH, INPUT_FILES_PATH)

import os
import pandas as pd


class Summary:
    pass


class TCGA:
    def __init__(self, cohort_name):
        self.cohort_name = str(cohort_name).upper()
        self.input_files_path = os.path.join(INPUT_FILES_PATH, self.cohort_name)
        self.chunks = self.get_input_files()
        self.downloaded_files_path = os.path.join(ELASPIC_RESULTS_FOLDER_PATH, self.cohort_name)
        self.chunks_to_num_downloaded_subchunks = self.get_chunks_to_num_downloaded_subchunks()
        self.chunks_to_num_active_computations = self.get_chunks_to_num_active_computations()

    def get_input_files(self):
        input_files = os.listdir(self.input_files_path)
        input_files_sorted = list(map(str, sorted(map(int, input_files))))
        return input_files_sorted

    def get_total_chunks(self):
        return len(os.listdir(os.path.join(INPUT_FILES_PATH, self.cohort_name)))

    def get_downloaded_subchunks(self, chunk):
        chunk_path = os.path.join(self.downloaded_files_path, chunk)
        try:
            return os.listdir(chunk_path)
        except FileNotFoundError:
            return []

    def get_chunks_to_num_active_computations(self):
        chunks_to_num_active_computations = dict.fromkeys(map(str, self.chunks))
        for chunk in self.chunks:
            record_filepath = rf'record_{self.cohort_name}_{chunk}.csv'
            record_path = os.path.join(RECORDS_FOLDER_PATH, self.cohort_name, record_filepath)
            record_data = pd.read_csv(record_path)
            num_active_computations = len(record_data[(record_data['UPLOADED_STATUS'] == 1) &
                                                      (record_data['DOWNLOADED_STATUS'] == 0)])

            chunks_to_num_active_computations[chunk] = num_active_computations

        return chunks_to_num_active_computations

    def get_chunks_to_num_downloaded_subchunks(self):
        chunks_to_num_downloaded_subchunks = dict.fromkeys(map(str, self.chunks))
        for chunk in self.chunks:
            chunks_to_num_downloaded_subchunks[chunk] = len(self.get_downloaded_subchunks(chunk))

        return chunks_to_num_downloaded_subchunks

    def get_summary_table(self):
        table = pd.DataFrame(self.chunks_to_num_downloaded_subchunks,
                             index=['Downloaded_subchunk']).T
        table.index.name = 'Chunk'
        table['NUM_ACTIVE_COMPUTATIONS'] = list(self.chunks_to_num_active_computations.values())

        return table

    def get_summary(self, print_table=True, subchunks_of=None, filter=None):
        print(f"SUMMARY FOR TCGA   : \t {self.cohort_name}")
        table = self.get_summary_table()
        chunks_remaining = len(table[table['Downloaded_subchunk'] == 0])
        print(f"CHUNKS DOWNLOADED  : \t {len(self.chunks) - chunks_remaining} / {len(self.chunks)}")
        if subchunks_of is not None:
            print("\tSUBCHUNKS OF {} : \t {} DOWNLOADED".format(
                subchunks_of, table.loc[str(subchunks_of), 'Downloaded_subchunk']))

        if print_table:
            table_all = table.copy()
            table_print = table.copy()
            print("SUMMARY TABLE      :\n")
            if filter:
                print("\t  - - -  (FILTERED) - - - ")
                table_print = table_print.iloc[filter, :]
            print(table_print)
            downloaded = table_all['Downloaded_subchunk'].sum()
            total = len(self.chunks) * 100
            print(f"Number of total downloaded subchunk files [{self.cohort_name}]: "
                  f"{downloaded} of {total}"
                  f" ({round((downloaded / total) * 100, 2)}%)")


ov = TCGA('OV')
filter_chunks = list(range(18, 22))
ov.get_summary(print_table=True)

# coad = TCGA('COAD')
# filter_chunks = list(range(0, 51))
# # filter_chunks = list(range(51, 101))
# # filter_chunks = list(range(90, 127))
# coad.get_summary(print_table=True, filter=filter_chunks)
# # coad.get_summary(print_table=True)

# OV: (69.69%)
# COAD: (30.74%)
