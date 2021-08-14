import logging
import os
import time
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(message)s')


# def wait(duration):
#     time_elasped = 0
#     while time_elasped < duration:
#         print('.', end='')
#         time.sleep(0.1)
#         time_elasped += 0.1
#     print()

def wait(duration):
    if duration == 0:
        return
    for _ in tqdm(range(duration), desc='[WAIT_DELAY]', position=0, leave=True):
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
