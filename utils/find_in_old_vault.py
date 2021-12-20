from datetime import datetime
from pathlib import Path

import pandas as pd
import os
import os.path as op
from tqdm import tqdm

import logging
from log_script import ColorHandler

pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

log = logging.Logger("debug_runner", level=logging.DEBUG)
log.addHandler(ColorHandler())

ELASPIC_INPUT_PATH = "../ELASPIC_Input/"
ELASPIC_RESULTS_PATH = "../Elaspic_Results/"


class FindInOldVault:
    def __init__(self, tcga, new_results_path, old_results_path):
        self.tcga = tcga.upper()
        log.info(f"Initializing FindInOldVault with TCGA: {self.tcga}")
        self.new_results_path = new_results_path
        self.old_results_path = old_results_path

        self.input_path = op.join(ELASPIC_INPUT_PATH, self.tcga)
        self.chunks = sorted(os.listdir(self.input_path))
        self.input_pairs = self.get_input_pairs()

        self.new_results = self.load_results(self.new_results_path)
        self.old_results = self.load_results(self.old_results_path)

        self.pairs_not_found = None
        self.pairs_found_in_vault = None

        self.rescued_data = None

        self.check_pairs()
        self.rescue_pairs()

        self.export_rescued_data()

        log.info("Process completed successfully.")

    def check_pairs(self):
        pairs_not_found = []
        pairs_found_in_vault = []
        for pair in tqdm(self.input_pairs):
            if not self.check_in_results(self.new_results, pair):
                pairs_not_found.append(pair)
                if self.check_in_results(self.old_results, pair):
                    pairs_found_in_vault.append(pair)

        log.debug(f"Num pairs not found = {len(pairs_not_found)}")
        log.debug(f"Num pairs rescued = {len(pairs_found_in_vault)}")

        self.pairs_not_found = pairs_not_found
        self.pairs_found_in_vault = pairs_found_in_vault

    def rescue_pairs(self):
        query_dataframes = []
        for pair in tqdm(self.pairs_found_in_vault):
            log.info(f"PAIR: {pair}")
            query = self.query(self.old_results, pair)
            query_dataframes.append(query)

        rescued_data = pd.concat(query_dataframes)
        log.debug(f"{rescued_data.shape=}")
        log.debug("\n{}".format(rescued_data.head()))

        self.rescued_data = rescued_data

    def get_input_pairs(self):
        pairs = set()
        for chunk in tqdm(self.chunks):
            chunk_path = op.join(self.input_path, chunk)
            for subchunk in os.listdir(chunk_path):
                subchunk_path = op.join(chunk_path, subchunk)
                pairs.update(self.get_input_pairs_single_file(subchunk_path))
                # log.debug(chunk, subchunk)

        return pairs

    @staticmethod
    def get_input_pairs_single_file(file_path):
        with open(file_path) as file:
            pairs = [line.strip() for line in file.readlines()]

        return pairs

    @staticmethod
    def load_results(results_path):
        results_data = pd.read_csv(results_path, sep='\t', low_memory=False)
        # Ensure there are only "done" entries
        assert results_data["Status"].nunique() == 1
        [status_val] = results_data["Status"].unique()
        assert status_val == "done", status_val
        return results_data

    @staticmethod
    def query(results_data, pair):
        protein, mutation = pair.split('.')
        query = results_data[
            (results_data["UniProt_ID"] == protein) &
            (results_data["Mutation"] == mutation)
            ]
        return query

    def check_in_results(self, results_data, pair):
        query = self.query(results_data, pair)
        if query.empty:
            return False
        else:
            return True

    def export_rescued_data(self):
        rescued_folder_path = op.join(ELASPIC_RESULTS_PATH, self.tcga, "rescued")
        Path(rescued_folder_path).mkdir(parents=True, exist_ok=True)
        rescued_data_path = op.join(rescued_folder_path, f"{self.tcga}_rescued.txt")

        if op.isfile(rescued_data_path):
            log.warning("You already have the file.")
            raise FileExistsError("You already have the file.")

        else:
            self.rescued_data.to_csv(rescued_data_path, sep='\t', index=False)
            log.info(f"Rescued data for {self.tcga} is exported.")


OLD_VAULT_PATH = r"../Elaspic_Results/Vault/old_merged_core_interface_vault_2021-11-17.txt"

BRCA_MERGED_INTERFACE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/BRCA_Interface_2021-11-17_without_rescued.txt"
BRCA_MERGED_CORE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/BRCA_Core_2021-11-17_without_rescued.txt"

OV_MERGED_INTERFACE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/OV_Interface_2021-11-17_without_rescued.txt"
OV_MERGED_CORE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/OV_Core_2021-11-17_without_rescued.txt"

ESCA_MERGED_INTERFACE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/ESCA_Interface_2021-11-17-wr.txt"
ESCA_MERGED_CORE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/ESCA_Core_2021-11-17-wr.txt"

HNSC_MERGED_INTERFACE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/HNSC_Interface_2021-11-17-wr.txt"
HNSC_MERGED_CORE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/HNSC_Core_2021-11-17-wr.txt"

GBM_MERGED_INTERFACE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/GBM_Interface_2021-11-17-wr.txt"
GBM_MERGED_CORE_RESULTS_PATH = r"../Elaspic_Results/Merged_Results/GBM_Core_2021-11-17-wr.txt"




def combine_core_interface(tcga, core_data_path, interface_data_path):
    core_data = pd.read_csv(core_data_path, sep='\t', low_memory=False)
    interface_data = pd.read_csv(interface_data_path, sep='\t', low_memory=False)
    core_and_interface_data = pd.concat([core_data, interface_data])
    data_date = datetime.today().strftime('%Y-%m-%d')
    core_and_interface_data_path = (
        f"../Elaspic_Results/Merged_Results/core_interface_combined/{tcga}_core_and_interface_combined_{data_date}.txt"
    )
    if op.isfile(core_and_interface_data_path):
        log.warning("You already have the file.")
        raise FileExistsError("You already have the file.")

    else:
        core_and_interface_data.to_csv(core_and_interface_data_path, sep='\t', index=False)
        log.info(f"core_and_interface_data for {tcga} is exported.")


# combine_core_interface("BRCA", BRCA_MERGED_CORE_RESULTS_PATH, BRCA_MERGED_INTERFACE_RESULTS_PATH)
# combine_core_interface("OV", OV_MERGED_CORE_RESULTS_PATH, OV_MERGED_INTERFACE_RESULTS_PATH)
# combine_core_interface("ESCA", ESCA_MERGED_CORE_RESULTS_PATH, ESCA_MERGED_INTERFACE_RESULTS_PATH)
# combine_core_interface("HNSC", HNSC_MERGED_CORE_RESULTS_PATH, HNSC_MERGED_INTERFACE_RESULTS_PATH)
# combine_core_interface("GBM", GBM_MERGED_CORE_RESULTS_PATH, GBM_MERGED_INTERFACE_RESULTS_PATH)
# quit()
# # #

BRCA_COMBINED_RESULTS_PATH = (
    r"../Elaspic_Results/Merged_Results/core_interface_combined/BRCA_core_and_interface_combined_2021-11-17.txt"
)
OV_COMBINED_RESULTS_PATH = (
    r"../Elaspic_Results/Merged_Results/core_interface_combined/OV_core_and_interface_combined_2021-11-17.txt"
)
ESCA_COMBINED_RESULTS_PATH = (
    r"../Elaspic_Results/Merged_Results/core_interface_combined/ESCA_core_and_interface_combined_2021-11-17.txt"
)
HNSC_COMBINED_RESULTS_PATH = (
    r"../Elaspic_Results/Merged_Results/core_interface_combined/HNSC_core_and_interface_combined_2021-11-17.txt"
)
GBM_COMBINED_RESULTS_PATH = (
    r"../Elaspic_Results/Merged_Results/core_interface_combined/GBM_core_and_interface_combined_2021-11-17.txt"
)

# FindInOldVault #

tcga_to_merged_interface_path = {
    # "BRCA": BRCA_COMBINED_RESULTS_PATH,
    # "OV": OV_COMBINED_RESULTS_PATH,
    # "ESCA": ESCA_COMBINED_RESULTS_PATH,
    # "HNSC": HNSC_COMBINED_RESULTS_PATH
    "GBM": GBM_COMBINED_RESULTS_PATH,
}

for tcga, merged_path in tcga_to_merged_interface_path.items():
    FindInOldVault(tcga, merged_path, OLD_VAULT_PATH)
    log.info("exiting ..")
    quit()


"""
1. run merge results E.g. BRCA 61 chunks are merged.
2. run `combine_core_interface` function only.
3. comment out `combine_core_interface` and run `FindInOldVault`.
   this will create a `rescued` folder in that tcga. e.g. as an 62nd folder.
4. now you can delete old merged results (core and interface) and re run merge results. 
   this will now take the `rescued` folder into account. 

Hence we will have obtained the missing features.

"""

