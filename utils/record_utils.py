import pandas as pd
from utils.organizer import parse_filename
import os
import logging
from config import ALLMUTATIONS_FAILED_PATH


def read_record_data(record_filepath):
    data = pd.read_csv(record_filepath, index_col='filename')
    return data


def create_initial_data(record_filepath):
    logging.debug('creating records for failed mutations.')
    data = get_entry_initial_data()
    data.to_csv(record_filepath)


def save_record_data(data, record_filepath):
    logging.debug('saving records for failed mutations. (written on disk).')
    data.to_csv(record_filepath)


def get_entry_initial_data():
    initial_data = pd.DataFrame({"filename": [],
                                 "URLs": []}).set_index('filename')

    return initial_data


def get_entry_data(filename, url):
    entry_data = pd.DataFrame({"filename": [filename],
                               "URLs": [url]}).set_index('filename')

    return entry_data


def add_entry(data, filename, url):
    data = data.append(get_entry_data(filename, url))
    return data


def append_url(data, filename, new_url):
    old_urls = data.loc[filename, 'URLs']
    data.loc[filename, 'URLs'] = ' - '.join([old_urls, new_url])
    return data


def filename_already_recorded(data, filename):
    return filename in data.index


def record_file_exist(filepath):
    return os.path.isfile(filepath)


def record_allmutations_failed(filename, url, allmutations_failed_path=ALLMUTATIONS_FAILED_PATH):
    tcga_code, _, _ = parse_filename(filename)

    logging.debug(f'filename: {filename}')
    logging.debug(f'allmutations_failed_path: {allmutations_failed_path}')

    allmutations_failed_path = os.path.join(allmutations_failed_path, tcga_code + '.csv')
    if not record_file_exist(allmutations_failed_path):
        logging.info(f"Creating allmutations results fail record file {allmutations_failed_path}")
        create_initial_data(allmutations_failed_path)

    allmutations_failed_record_data = read_record_data(allmutations_failed_path)

    if filename_already_recorded(allmutations_failed_record_data, filename):
        logging.info('filename already recorded as allmutations_failed, appending the url.')
        allmutations_failed_record_data = append_url(allmutations_failed_record_data, filename, url)

    else:
        print('recording new filename for allmutations_failed ..')
        allmutations_failed_record_data = add_entry(allmutations_failed_record_data, filename, url)

    save_record_data(allmutations_failed_record_data, allmutations_failed_path)

# if __name__ == '__main__':
#     record_allmutations_failed('SNV_ABE_Chunk_92_0.txt', 'url00', '')
#     record_allmutations_failed('SNV_ABE_Chunk_92_1.txt', 'url11', '')
#     record_allmutations_failed('SNV_ABE_Chunk_92_2.txt', 'url22', '')
