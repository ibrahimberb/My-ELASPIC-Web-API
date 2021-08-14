import logging
import os
import shutil
from pathlib import Path
import pathlib
import glob

logging.basicConfig(level=logging.INFO, format='%(message)s')


def parse_filename(filepath):
    """
    Parses the filepath

    Parameters
    ----------
        filepath : <todo>
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


def move_file(downloaded_folder_path, tcga_code, chunk_no, subchunk_no, downloaded_filename):
    """Moves the file where it belongs."""

    files = glob.glob(os.path.join(downloaded_folder_path, downloaded_filename))
    # Ensure there is 1 file to be moved.
    assert len(files) == 1
    downloaded_file_path = files[0]

    correct_folder_path = pathlib.Path().resolve() / "ELASPIC_Results" / tcga_code
    correct_filename = f"allresults_{tcga_code}_{chunk_no}_{subchunk_no}.txt"
    correct_file_path = os.path.join(correct_folder_path, correct_filename)

    # Create paths
    Path(correct_folder_path).mkdir(parents=True, exist_ok=True)

    if os.path.isfile(correct_file_path):
        raise FileExistsError(f"You already have the file {correct_filename}")

    logging.debug('downloaded_file_path:', downloaded_file_path)
    logging.debug('correct_file_path:', correct_file_path)

    logging.info('Moving the file to correct location ..')
    shutil.move(downloaded_file_path, correct_file_path)


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
