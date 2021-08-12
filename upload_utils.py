from utils import is_valid_file
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def upload_file(driver, upload_file_path):
    # Upload the file.
    upload_file_button = driver.find_element_by_id("pfile")
    assert is_valid_file(upload_file_path), 'check your file!'
    upload_file_button.send_keys(upload_file_path)
    logging.info('Uploaded file: {}'.format(upload_file_path))
