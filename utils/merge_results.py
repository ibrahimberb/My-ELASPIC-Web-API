# Merge subchunks into single data.
from datetime import datetime
from pathlib import Path

import pandas as pd
import os
import glob
from tqdm import tqdm

import seaborn as sns
import matplotlib.pyplot as plt

from config import ELASPIC_RESULTS_FOLDER_PATH as ERFP

import logging
from log_script import ColorHandler

pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

log = logging.Logger("debug_runner", level=logging.DEBUG)
log.addHandler(ColorHandler())


class ResultsMerger:
    """
    There might be still duplicated entries once it is read by pandas.
    """
    ELASPIC_RESULTS_FOLDER_PATH = os.path.join("..", ERFP)

    def __init__(self, tcga):

        log.info(f" --- Starting ResultsMerger for {tcga}.. --- ")

        self.tcga = tcga
        self.data_concated = self.concatenate_results()
        self.type_counts = self.get_type_counts()

        self.plot_type_distribution(self.data_concated)

        core_data, interface_data = self.separate_core_interface()
        self.core_data = core_data
        self.interface_data = interface_data

        # Handle core mutations
        self.core_data_dropped = self.drop_duplicates(self.core_data)

        # Handle interface mutations
        self.interface_data_no_self_interactions = self.drop_self_interactions(self.interface_data)
        self.interface_data_dropped = self.drop_duplicates(self.interface_data_no_self_interactions)

        raise Exception("uncomment export functions!")
        # self.export(self.core_data_dropped, f"{self.tcga}_Core")
        # self.export(self.interface_data_dropped, f"{self.tcga}_Interface")

        log.info("Results are merged and exported successfully.\n")

    def concatenate_results(self):
        """
        Concatenates result text files into single dataframe for given TCGA type.
        """

        log.info("Concatenating the results ..")

        result_dataframes = []
        chunks_path = os.path.join(self.ELASPIC_RESULTS_FOLDER_PATH, self.tcga)
        chunks = os.listdir(chunks_path)
        num_data_combined = 0
        log.debug("Reading the files ..")
        for chunk in tqdm(chunks):
            subchunks_path = os.path.join(self.ELASPIC_RESULTS_FOLDER_PATH, self.tcga, chunk, Path('*'))
            for subchunk_path in glob.glob(subchunks_path):
                # log.debug(f"reading {subchunk_path} ..")
                subchunk_data = pd.read_table(subchunk_path, low_memory=False)
                result_dataframes.append(subchunk_data)
                num_data_combined += 1

        log.debug('{} files are loaded.'.format(num_data_combined))

        log.debug("Concatenating dataframes into single dataframe ..")
        concated_data = pd.concat(result_dataframes).reset_index(drop=True)

        # Drop entries where status is not 'done' (either 'err' or 'running'), i.e. keep only "done" entries.
        concated_data = concated_data[concated_data["Status"] == "done"]

        log.info("Datasets are concatenated.")

        log.debug(f"concated_data.shape: {concated_data.shape}")
        log.debug(f"First five rows in concated_data: \n{concated_data.head()}")
        log.debug(f"Unique values in concated_data['Type']: {list(concated_data['Type'].unique())}")

        return concated_data

    def get_type_counts(self):
        type_counts = pd.DataFrame({
            f"{self.tcga}": self.data_concated["Type"].value_counts()
        })
        log.info(f"type_counts: \n{type_counts}")

        return type_counts

    @staticmethod
    def get_entries_core(data):
        core_data = data[data["Type"] == 'core'].reset_index(drop=True)
        return core_data

    @staticmethod
    def get_entries_interface(data):
        interface_data = data[data["Type"] == 'interface'].reset_index(drop=True)
        return interface_data

    def separate_core_interface(self):
        """Returns Core Data and Interface Data"""
        log.debug("Separating Core and Interface entries ..")
        core_data = self.get_entries_core(self.data_concated)
        interface_data = self.get_entries_interface(self.data_concated)

        log.debug(f"Core data dimensions: {core_data.shape}")
        log.debug(
            "Core data preview: \n{}\n".format(
                core_data[["UniProt_ID", "Mutation", "Interactor_UniProt_ID"]].head(3)
            )
        )

        log.debug(f"Interface data dimensions: {interface_data.shape}")
        log.debug(
            "Interface data preview: \n{}\n".format(
                interface_data[["UniProt_ID", "Mutation", "Interactor_UniProt_ID"]].head(3)
            )
        )

        return core_data, interface_data

    @staticmethod
    def drop_self_interactions(data):
        """
        Entries whose UniProt_ID protein is the same (or isoform) as Interactor_UniProt_ID will be removed.
        """

        log.debug("Dropping self interactions ..")

        # Take the entries where UniProt_ID different than Interactor_UniProt_ID (dropping self and isoform)
        data_dropped = data[
            data["UniProt_ID"].apply(lambda x: x.split('-')[0]) != data["Interactor_UniProt_ID"].apply(lambda x: x.split('-')[0])
        ]

        # Reset index of the dataframe to avoid any possible errors
        data_dropped = data_dropped.reset_index(drop=True)

        return data_dropped

    @staticmethod
    def drop_duplicates(data):
        """
        Remove duplicated entries in the given dataframe.
        """

        log.debug("Dropping duplicated entries ..")

        # Size of dataframe before dropping duplicated entries.
        log.debug(f"Size of dataframe before dropping duplicated entries: {data.shape}")

        # Drop duplicates by keeping the 'first' one.
        data = data.drop_duplicates(keep="first")

        # Size of dataframe after dropping duplicated entries.
        log.debug(f"Size of dataframe  after dropping duplicated entries: {data.shape}")

        # Reset index of the dataframe to avoid any possible errors
        data.reset_index(drop=True, inplace=True)

        return data

    def export(self, data, data_name):
        current_date = datetime.today().strftime('%Y-%m-%d')
        filename = f"{data_name}_{current_date}.txt"
        folder_path = os.path.join(self.ELASPIC_RESULTS_FOLDER_PATH, "Merged_Results")
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        filepath = os.path.join(folder_path, filename)

        if os.path.isfile(filepath):
            raise FileExistsError("You have already exported predictions! Clear the folder.")

        data.to_csv(filepath, sep='\t', index=False)
        log.info(f"Data {filename} is exported in directory {filepath}.")

    def plot_type_distribution(self, data):
        plt.figure(figsize=(7, 5))
        sns.set(style="white", font_scale=1.15)  # white, dark, whitegrid, darkgrid, ticks
        ax = sns.barplot(
            x=data["Type"].value_counts().index,
            y=data["Type"].value_counts(),
            palette="vlag_r"
        )
        ax.set_title('Distribution of `Core` vs `Interface`\nin {}'.format(self.tcga))  # ch:s=-.2,r=.6, ocean
        ax.set_xlabel('Type', fontsize=14)
        ax.set_ylabel('Count', fontsize=14)
        plt.show()


ResultsMerger(tcga="BRCA")
ResultsMerger(tcga="OV")
