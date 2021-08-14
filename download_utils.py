import os
import time
import logging
from page_utils import click_button_by_xpath

logging.basicConfig(level=logging.INFO, format='%(message)s')


def download_result_file(driver, download_folder_path):
    click_button_by_xpath(driver, element_xpath='// *[ @ id = "allresults"] / a')
    wait_result_download(download_folder_path)


def wait_result_download(dir_name, filename="allresults.txt", timeout_duration=15):
    logging.debug("dir_name:", dir_name)
    download_file_path = os.path.join(dir_name, filename)
    logging.debug("download_file_path:", download_file_path)
    time_elapsed = 0
    while not os.path.exists(download_file_path):
        if time_elapsed > timeout_duration:
            break
        time.sleep(1)
        time_elapsed += 1
    if os.path.isfile(download_file_path):
        logging.info('File is downloaded.')
    else:
        logging.warning('file still not downloaded.')
        # break operation.

    time.sleep(0.5)
