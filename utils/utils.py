import logging
import os
import time
from typing import Union

from tqdm import tqdm
from config import (
    UPLOAD_FAILED_PATH,
    UNEXPECTED_FAILED_PATH,
    ALLMUTATIONS_FAILED_PATH,
    TEMP_DOWNLOAD_FOLDER_PATH,
    CHUNKS_TO_RUN_FOLDER_PATH
)

import glob
from utils.organizer import parse_filename
import pandas as pd
from time import localtime, strftime

logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_current_time():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def get_subchunk_files(subchunks_path, tcga=None, chunk_no=None):
    if tcga is not None:
        subchunks_path = os.path.join(os.getcwd(), subchunks_path, tcga, str(chunk_no), '*')
    else:
        subchunks_path = os.path.join(os.getcwd(), subchunks_path, '*')

    logging.info(f"subchunks_path: {subchunks_path}")
    files = [file for file in
             glob.glob(subchunks_path)
             if '.txt' in file]
    # logging.info(f"FILES: {files}")
    return files


Seconds = Union[int, float]


def wait(duration: Seconds, desc=None):
    if desc is None:
        desc = "[WAIT_DELAY]"
    if duration == 0:
        return
    if duration <= 1:
        time.sleep(duration)

    elif isinstance(duration, int):
        for _ in tqdm(range(duration), desc=desc, position=0, leave=True):
            time.sleep(1)

    else:
        time.sleep(duration)


def is_valid_file(filepath):
    with open(filepath) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip() != '']

    logging.debug('number of lines {}'.format(len(lines)))
    return len(lines) > 0


def get_filename_from_path(filepath):
    filename = os.path.basename(filepath)
    return filename


def record_upload_failed(filename, upload_failed_path=UPLOAD_FAILED_PATH):
    record_bad_states(filename, "upload fail", upload_failed_path)


def delete_allresults_temp_file(temp_download_folder_path=TEMP_DOWNLOAD_FOLDER_PATH):
    allresults_temp_filepath = os.path.join(temp_download_folder_path, 'allresults.txt')
    if os.path.isfile(allresults_temp_filepath):
        logging.info(f'removing temp allresults file: {allresults_temp_filepath}')
        os.remove(allresults_temp_filepath)
    else:
        print("Error: {} file not found.".format(allresults_temp_filepath))


# deprecated
def record_allmutations_failed(filename, url, allmutations_failed_path=ALLMUTATIONS_FAILED_PATH):
    # The webpage says "All the mutations are done!" but all entries have cross,
    # indicating the ERR.
    tcga_code, _, _ = parse_filename(filename)
    allmutations_failed_path = os.path.join(allmutations_failed_path, tcga_code + '.csv')
    if not os.path.isfile(allmutations_failed_path):
        logging.info(f"Creating allmutations results fail record file {allmutations_failed_path}")
        allmutations_failed_record_data = pd.DataFrame({"filename": [],
                                                        "URLs": []})

    with open(allmutations_failed_path) as file:
        lines = file.readlines()
        filenames = [line.split('-')[0].strip() for line in lines]
        if filename in filenames:
            logging.info(f"{filename} already recorded as allmutations results fail.")
            logging.info(f"Appending the new failed URL.")
            return

    with open(allmutations_failed_path, 'a') as file:
        logging.info(f"Recording {filename} as failed ..")
        file.write(f"{filename}\n")


def record_unexpected_failed(filename, unexpected_failed_path=UNEXPECTED_FAILED_PATH):
    record_bad_states(filename, "unexpected fail", unexpected_failed_path)


def record_bad_states(filename, bad_state, bad_state_path):
    tcga_code, _, _ = parse_filename(filename)
    bad_state_path = os.path.join(bad_state_path, tcga_code + '.txt')
    if not os.path.isfile(bad_state_path):
        logging.info(f"Creating {bad_state} record file {bad_state_path}")
        with open(bad_state_path, 'w'): pass

    with open(bad_state_path) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        if filename in lines:
            logging.info(f"{filename} already recorded as {bad_state}.")
            return

    with open(bad_state_path, 'a') as file:
        logging.info(f"Recording {filename} as failed ..")
        file.write(f"{filename}\n")


def read_chunks_to_run(tcga):
    filepath = os.path.join(CHUNKS_TO_RUN_FOLDER_PATH, f"chunks_to_run_{tcga.upper()}.txt")
    with open(filepath, 'r') as file:
        chunks = [int(line.strip()) for line in file.readlines()]

    return chunks
