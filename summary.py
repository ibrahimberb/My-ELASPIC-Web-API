# August 16, 2021
from typing import List
import logging

from config import (
    RECORDS_FOLDER_PATH,
    ELASPIC_RESULTS_FOLDER_PATH,
    INPUT_FILES_PATH,
    CHUNKS_TO_RUN_FOLDER_PATH,
)

import os
import pandas as pd
import os.path as op

logging.basicConfig(level=logging.INFO, format='%(message)s')

pd.set_option('display.max_rows', 500)


def write_to_file(tcga: str, chunks: List[int]):
    filepath = op.join(CHUNKS_TO_RUN_FOLDER_PATH, f'chunks_to_run_{tcga}.txt')
    with open(filepath, 'w') as file:
        for chunk in chunks[:-1]:  # Exclude the last chunk
            file.write(f"{chunk}\n")

    print(f"Chunks for {tcga} are exported to file {filepath}")


class Summary:
    def __init__(self, tcga):
        self.tcga = str(tcga).upper()
        self.input_files_path = op.join(INPUT_FILES_PATH, self.tcga)
        self.chunks = self.get_input_files()
        self.downloaded_files_path = op.join(ELASPIC_RESULTS_FOLDER_PATH, self.tcga)
        self.chunks_to_num_downloaded_subchunks = self.get_chunks_to_num_downloaded_subchunks()
        self.chunks_to_num_active_computations = self.get_chunks_to_num_active_computations()

    def get_input_files(self):
        input_files = os.listdir(self.input_files_path)
        logging.warning(input_files)
        logging.warning(f"{self.input_files_path}")
        input_files_sorted = list(map(str, sorted(map(int, input_files))))
        return input_files_sorted

    def get_total_chunks(self):
        return len(os.listdir(op.join(INPUT_FILES_PATH, self.tcga)))

    def get_downloaded_subchunks(self, chunk):
        chunk_path = op.join(self.downloaded_files_path, chunk)
        try:
            return os.listdir(chunk_path)
        except FileNotFoundError:
            return []

    def get_chunks_to_num_active_computations(self):
        chunks_to_num_active_computations = dict.fromkeys(map(str, self.chunks))
        for chunk in self.chunks:
            record_filepath = rf'record_{self.tcga}_{chunk}.csv'
            record_path = op.join(RECORDS_FOLDER_PATH, self.tcga, record_filepath)
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

    def get_summary(
            self,
            print_table=True,
            subchunks_of=None,
            filter_=None,
            threshold=90,
            active_computations_only=False,
            export=False
    ):
        print(f"SUMMARY FOR TCGA   : \t {self.tcga}")
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
            if filter_:
                filter_ = [e - 1 for e in filter_]
                print("\t  - - -  (FILTERED) - - - ")
                table_print = table_print.iloc[filter_, :]
            print(table_print)
            downloaded = table_all['Downloaded_subchunk'].sum()
            total = len(self.chunks) * 100
            print(f"Number of total downloaded subchunk files [{self.tcga}]: "
                  f"{downloaded} of {total}"
                  f" ({round((downloaded / total) * 100, 2)} %)")

            table_above_thr = table_all[table_all["Downloaded_subchunk"] >= threshold]
            table_above_thr_chunks = list(map(int, table_above_thr.index))
            table_below_thr = table_all[table_all["Downloaded_subchunk"] < threshold]
            table_below_thr_chunks = list(map(int, table_below_thr.index))
            print(f"Chunks with downloaded sub-chunk {threshold} or above:\n"
                  f"{table_above_thr_chunks}")
            print(f"Chunks with downloaded sub-chunk below {threshold}:\n"
                  f"{table_below_thr_chunks}")
            below_thr_ix = [e - 1 for e in table_below_thr_chunks]
            table_print_below_thr = table_all.iloc[below_thr_ix, :]

            if active_computations_only:
                print(f"\n\t  - - -  BELOW THRESHOLD {threshold} (Filtered for Active Computations) - - - ")
                table_print_below_thr = table_print_below_thr[
                    table_print_below_thr["NUM_ACTIVE_COMPUTATIONS"] > 0
                    ]

            else:
                print(f"\n\t  - - -  (BELOW THRESHOLD {threshold}) - - - ")

            print(table_print_below_thr)

            if export:
                if active_computations_only:
                    write_to_file(self.tcga, table_print_below_thr.index)
                else:
                    write_to_file(self.tcga, table_below_thr_chunks)

    def bring_record(self, chunk_no):
        record_path = op.join(
            RECORDS_FOLDER_PATH, self.tcga, f"record_{self.tcga}_{chunk_no}.csv"
        )
        print(f"record_path: {record_path}")

        record = pd.read_csv(record_path)

        active_urls = record[
            (record["UPLOADED_STATUS"] == 1) &
            (record["DOWNLOADED_STATUS"] == 0)
            ]["ELASPIC_URL"]
        print(f"ACTIVE URLS: \n{active_urls}")


# coad = TCGA('COAD')
# coad.get_summary(
#     print_table=True,
#     threshold=90
# )

# coad = TCGA('PAAD')
# coad.get_summary(
#     print_table=True,
#     threshold=90
# )

# don't worry about remaining active inputs if above 90 %
# BRCA  :  5761 of  6100 (94.44 %)
# OV    :  3654 of  3900 (93.69 %)
# ESCA  :  1872 of  2000 (93.6 %)
# HNSC  :  5039 of  5500 (91.62 %)
# GBM   :  4539 of  4700 (96.57 %)
# BLCA  :  6988 of  7300 (95.73 %)
# COAD  :  11438 of 12700 (90.06 %)
# - - - - - - - - - - - - - - - - - - - -

#####################
# # # COMPLETED # # #
# tcga = "BRCA"
# tcga = "OV"
# tcga = "ESCA"
# tcga = "HNSC"
# tcga = "GBM"
# tcga = "BLCA"
# tcga = "COAD"
# ---------------
####################

tcga = "BLCA"

Summary(tcga).get_summary(
    print_table=True,
    threshold=90,  # 90
    export=True,
    active_computations_only=False
)

# Summary(tcga).bring_record(20)
# Summary(tcga).bring_record(38)
# Summary(tcga).bring_record(44)
#
# # next cohort??
#
# LOOK_UP_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\ELASPIC_Input\GBM\20"
# print(f"Number of subchunks {len(os.listdir(LOOK_UP_PATH))}")
