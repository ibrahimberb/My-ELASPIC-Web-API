# August 16, 2021

from config import (
    ELASPIC_RESULTS_FOLDER_PATH, RECORDS_FOLDER_PATH, ALLMUTATIONS_FAILED_PATH,
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

    def get_chunks_to_num_downloaded_subchunks(self):
        chunks_to_num_downloaded_subchunks = dict.fromkeys(map(str, self.chunks))
        for chunk in self.chunks:
            chunks_to_num_downloaded_subchunks[chunk] = len(self.get_downloaded_subchunks(chunk))

        return chunks_to_num_downloaded_subchunks

    def get_summary_table(self):
        table = pd.DataFrame(self.chunks_to_num_downloaded_subchunks,
                             index=['Downloaded_subchunk']).T
        table.index.name = 'Chunk'

        return table

    def get_summary(self, print_table=True, subchunks_of=None, filter=None):
        print(f"SUMMARY FOR TCGA   : \t {self.cohort_name}")
        table = self.get_summary_table()
        chunks_remaining = len(table[table['Downloaded_subchunk'] == 0])
        print(f"CHUNKS DOWNLOADED  : \t {len(self.chunks) - chunks_remaining} / {len(self.chunks)}")
        if subchunks_of is not None:
            print("\tSUBCHUNKS OF {} : \t {} DOWNLOADED".format(
                subchunks_of, table.loc[str(subchunks_of), 'Downloaded_subchunk']))

        if print_table and filter is None:
            print("SUMMARY TABLE      :\n")
            print(table)

        if print_table and filter is not None:
            table = table.iloc[filter, :]
            print("SUMMARY TABLE      :\n")
            print(table)


ov = TCGA('OV')
# ov.get_summary(print_table=False, subchunks_of=11)
ov.get_summary(print_table=True, filter=list(range(9, 20)))
