import logging
import os
import shutil
from pathlib import Path
import pathlib
import glob
from config import ELASPIC_RESULTS_FOLDER_PATH

logging.basicConfig(level=logging.INFO, format='%(message)s')


class CorrectLocation:
    def __init__(self, tcga_code, chunk_no, subchunk_no):
        self.tcga_code = tcga_code
        self.chunk_no = chunk_no
        self.subchunk_no = subchunk_no
        self.correct_folder_path = pathlib.Path().resolve() / ELASPIC_RESULTS_FOLDER_PATH / tcga_code
        self.correct_filename = f"{chunk_no}/allresults_{tcga_code}_{chunk_no}_{subchunk_no}.txt"
        self.correct_file_path = os.path.join(self.correct_folder_path, self.correct_filename)


def parse_filename(filepath):
    """
    Parses the filepath

    Parameters
    ----------
        filepath:
            Filepath of chunkfile. E.g. SNV_BRCA_Chunk_22_0_test.txt
    """
    # Extract filename from filepath
    filename = os.path.basename(filepath)
    filename = filename.replace('.txt', '')
    logging.debug(f"filename: {filename}")
    filename_splitted = filename.split('_')
    logging.debug(f"filename_splitted: {filename_splitted}")
    logging.debug(f"TCGA: {filename_splitted[1]}, CHUNK: {filename_splitted[3]}, SUBCHUNK: {filename_splitted[4]}")

    tcga_code, chunk_no, subchunk_no = filename_splitted[1], filename_splitted[3], filename_splitted[4]

    return tcga_code, chunk_no, subchunk_no


def get_correct_location_obj(tcga_code, chunk_no, subchunk_no):
    correct_location_obj = CorrectLocation(tcga_code, chunk_no, subchunk_no)
    return correct_location_obj


def move_file(downloaded_folder_path, tcga_code, chunk_no, subchunk_no, downloaded_filename):
    """Moves the file where it belongs."""

    files = glob.glob(os.path.join(downloaded_folder_path, downloaded_filename))
    # Ensure there is 1 file to be moved.
    assert len(files) == 1
    downloaded_file_path = files[0]

    correct_location = CorrectLocation(tcga_code, chunk_no, subchunk_no)

    # Create paths
    Path(correct_location.correct_folder_path).mkdir(parents=True, exist_ok=True)

    if os.path.isfile(correct_location.correct_file_path):
        raise FileExistsError(f"You already have the file {correct_location.correct_file_path}")

    logging.debug('downloaded_file_path:', downloaded_file_path)
    logging.debug('correct_file_path:', correct_location.correct_file_path)

    logging.info('Moving the file to correct location ..')
    shutil.move(downloaded_file_path, correct_location.correct_file_path)


def is_file_located(filename):
    tcga_code, chunk_no, subchunk_no = parse_filename(filename)
    cl = CorrectLocation(tcga_code, chunk_no, subchunk_no)
    logging.debug(f'checking if {cl.correct_filename} exist.')
    return os.path.isfile(cl.correct_file_path)


# def clean_download_folder(downloaded_folder_path, downloaded_filename):
#     print("downloaded_folder_path:", downloaded_folder_path)
#     files = glob.glob(os.path.join(downloaded_folder_path, downloaded_filename))
#     print("WARNING: THIS FILES WILL BE REMOVED")
#     print(files)
#     # Ensure there is 1 file to be removed.
#     assert len(files) == 1
#     file = files[0]
#     os.remove(file)
#     logging.info(f"File is removed.")


def organize(downloaded_folder_path, input_file_path, downloaded_filename):
    logging.info('Organizing file location ..')
    input_file = os.path.basename(input_file_path)
    tcga_code, chunk_no, subchunk_no = parse_filename(input_file)
    move_file(downloaded_folder_path, tcga_code, chunk_no, subchunk_no, downloaded_filename)
    # clean_download_folder(downloaded_folder_path, downloaded_filename)
