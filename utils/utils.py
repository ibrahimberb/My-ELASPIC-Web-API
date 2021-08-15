import logging
import os
import time
from tqdm import tqdm
from config import UPLOAD_FAILED_PATH, UNEXPECTED_FAILED_PATH
import glob
from utils.organizer import parse_filename

logging.basicConfig(level=logging.INFO, format='%(message)s')


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


def wait(duration, desc=None):
    if desc is None:
        desc = "[WAIT_DELAY]"
    if duration == 0:
        return
    if duration <= 1:
        time.sleep(duration)

    else:
        for _ in tqdm(range(duration), desc=desc, position=0, leave=True):
            time.sleep(1)


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


def record_unexpected_failed(filename, unexpected_failed_path=UNEXPECTED_FAILED_PATH):
    record_bad_states(filename, "unexpected fail", unexpected_failed_path)


def record_bad_states(filename, bad_state, bad_state_path=UPLOAD_FAILED_PATH):
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
