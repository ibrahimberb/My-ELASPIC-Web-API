import logging
import os
import time
from tqdm import tqdm
from config import UPLOAD_FAILED_PATH
import glob

logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_subchunk_files(chunk_path):
    files = [file for file in
             glob.glob(chunk_path)
             if f'Chunk_{TODO}' in file]


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
    if not os.path.isfile(upload_failed_path):
        logging.info(f"Creating upload fail record file {upload_failed_path}")
        with open(upload_failed_path, 'w'): pass

    with open(upload_failed_path) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        if filename in lines:
            logging.info(f"{filename} already recorded as failed.")
            return

    with open(upload_failed_path, 'a') as file:
        logging.info(f"Recording {filename} as failed ..")
        file.write(f"{filename}\n")
