# -*- coding: UTF-8 -*-

# Imports
import logging

from upload_utils import upload_file
from organizer import organize, is_file_located
from config import DOWNLOAD_FOLDER_PATH, RECORDS_FOLDER_PATH, ELASPIC_MANY_URL
from download_utils import download_result_file
from driver_conf import initialize_driver
from record import get_chunk_record_status, Record, RecordStatuses
from interact_page import get_post_info
from utils import get_filename_from_path, wait
from page_utils import page_computation, ResponseMessages, process_input_recognization
from chunk import Chunk, make_chunk
import sys

logging.basicConfig(level=logging.INFO, format='[MyScapper] %(message)s')


class MyScraper:
    DEBUG_DELAY = 0

    def __init__(self, chunk_file_path, take_it_slow=False):
        self.chunk_file_path = chunk_file_path
        self.chunk_file_name = get_filename_from_path(self.chunk_file_path)
        self.ELASPIC_TARGET_URL = ELASPIC_MANY_URL
        self.run_mode = None
        self.driver = None
        self.chunk = Chunk()
        # self.already_calculated = None
        if take_it_slow:
            self.DEBUG_DELAY = 5
        logging.info('= = = = = = = = = = = = = = = = = = = = = =')
        logging.info("STARTING MyScraper ..")
        logging.info(f"FILENAME: {self.chunk_file_name} ")
        self.set_run_mode()
        self.run()

    def set_run_mode(self):
        record_response, chunk = get_chunk_record_status(self.chunk_file_path, "Records_Test")
        logging.info("RECORD STATUS: {}".format(record_response))
        self.run_mode = record_response
        # print('NEW COMING CHUNK URL:', chunk.elaspic_url)
        self.chunk = chunk

        # if self.run_mode == RecordStatuses.RECORDED_DOWNLOADED:
        #     logging.info(f'File {self.chunk_file_name} is already downloaded.')
        #     self.already_calculated = True

    def _initialize_driver(self):
        self.driver = initialize_driver()

    def open_recorded_page(self):
        self.driver.get(self.chunk.elaspic_url)
        # logging.info("Webpage Title: {}".format(self.driver.title))

    def open_default_page(self):
        self.driver.get(self.ELASPIC_TARGET_URL)
        # logging.info("Webpage Title: {}".format(self.driver.title))

    def run(self):
        # if self.already_calculated and is_file_located(self.chunk_file_name):
        #     print('file is located! doing nothing..')
        #     return

        # logging.info(f"Processing {self.chunk_file_path}")

        # if self.run_mode == RecordStatuses.RECORDED_DOWNLOADED:
        #     logging.info(f'File {self.chunk_file_name} is already downloaded.')
        #     self.driver.quit()
        #     return

        if self.run_mode == RecordStatuses.RECORDED_NOT_DOWNLOADED:
            self._initialize_driver()
            # record = Record(RECORDS_FOLDER_PATH, Chunk(file_path=self.chunk_file_path))
            # record.record()
            chunk = self.chunk
            self.open_recorded_page()

        elif self.run_mode == RecordStatuses.NOT_RECORDED:
            self._initialize_driver()
            logging.debug('uploading first time.')
            self.open_default_page()
            upload_file(self.driver, self.chunk_file_path)
            # Wait until all inputs are recognized.
            correctly_input_mutations_flag = process_input_recognization(self.driver)
            chunk = make_chunk(self.driver, file_path=self.chunk_file_path,
                               correctly_input_mutations_flag=correctly_input_mutations_flag)

            # Click on submit
            wait(self.DEBUG_DELAY)  # ------------------------------------------------
            self.driver.find_element_by_id('submit').click()
            logging.info('Clicking SUBMIT button ..')

        elif self.run_mode == RecordStatuses.RECORDED_DOWNLOADED:
            if is_file_located(self.chunk_file_name):
                logging.info('file is located! doing nothing..')
                return
            else:
                logging.info('Record says file is downloaded, but I could not find it.')
                logging.info('Re-downloading from recorded URL.')
                self._initialize_driver()
                chunk = self.chunk
                self.open_recorded_page()

        else:
            print(self.run_mode)
            raise ValueError('run mode not defined properly.')

        # if self.run_mode == RecordStatuses.RECORDED_NOT_DOWNLOADED:
        #     record = Record(RECORDS_FOLDER_PATH, Chunk(file_path=self.chunk_file_path))
        #     record.record()
        #     chunk = record.make_chunk_from_record()

        # elif self.run_mode == RecordStatuses.NOT_RECORDED:
        #     # Upload the file.
        #     upload_file(self.driver, self.chunk_file_path)
        #     # Wait until all inputs are recognized.
        #     correctly_input_mutations_flag = process_input_recognization(self.driver)
        #     # make a chunk object.
        #     chunk = make_chunk(self.driver, file_path=self.chunk_file_path,
        #                        correctly_input_mutations_flag=correctly_input_mutations_flag)

        # Get current URL.
        chunk.set_url(self.driver.current_url)
        chunk.set_uploaded_status(True)

        logging.info("current_url: {}".format(self.driver.current_url))

        wait(self.DEBUG_DELAY)  # ------------------------------------------------

        response = page_computation(self.driver)
        if response == ResponseMessages.COMPLETED:
            # download the allresult file.
            download_result_file(self.driver, DOWNLOAD_FOLDER_PATH)
            # move downloaded file to folder where it belongs and organize naming etc.
            organize(DOWNLOAD_FOLDER_PATH, self.chunk_file_path, downloaded_filename='allresults.txt')
            chunk.set_downloaded_status(True)
            logging.debug(f'+ chunk_downloaded_status : {chunk.downloaded_status}')
            chunk.set_mutations_post_info(get_post_info(self.driver))
            logging.info('File is downloaded successfully.')
            # todo run checker code.

        elif response == ResponseMessages.STILL_PROCESSING:
            logging.info('Mutations are in process.')
            chunk.set_downloaded_status(False)

        # chunk.print_info()
        record = Record(RECORDS_FOLDER_PATH, chunk)
        record.record()

        wait(self.DEBUG_DELAY * 2)  # ------------------------------------------------

        self.driver.quit()
        # logging.info(f"PROCESS COMPLETED FOR {self.chunk_file_path}")
        # logging.info('= = = = = = = = = = = = = = = = = = = = = =')


if __name__ == '__main__':
    import glob
    from itertools import cycle

    TEST_FILES_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\OV_10_test\*"

    upload_test_file_paths = [file for file in
                              glob.glob(TEST_FILES_PATH)
                              if 'Chunk_1' in file]

    # print(upload_test_file_paths)

    ################## RUN OPTION, how many files you want to run?
    # todo run browser in the background, it always pops up.

    # running all OV?, got it.
    upload_test_file_paths = upload_test_file_paths[:]
    #
    # upload_test_file_paths = [file for file in
    #                           glob.glob(TEST_FILES_PATH)
    #                           if 'SNV_BRCA_Chunk_22_21.txt' in file]

    upload_test_file_paths_cycle = cycle(upload_test_file_paths)
    for file_path in upload_test_file_paths_cycle:
        myscapper = MyScraper(file_path, take_it_slow=False)
        # wait(2)

    print('<END>')
