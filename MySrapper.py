# -*- coding: UTF-8 -*-

# Imports
import logging

from utils.upload_utils import upload_file
from utils.organizer import organize, is_file_located
from config import TEMP_DOWNLOAD_FOLDER_PATH, RECORDS_FOLDER_PATH, ELASPIC_MANY_URL, INPUT_FILES_PATH
from utils.download_utils import download_result_file
from utils.driver_conf import initialize_driver
from record import get_chunk_record_status, Record, RecordStatuses
from utils.interact_page import get_post_info, uploaded
from utils.utils import get_filename_from_path, wait, record_upload_failed, get_subchunk_files
from utils.page_utils import page_computation, ResponseMessages, process_input_recognization
from chunk import Chunk, make_chunk
from log_script import ColorHandler

log = logging.Logger('debug_runner', level=logging.DEBUG)
log.addHandler(ColorHandler())


class MyScraper:
    DEBUG_DELAY = 0

    def __init__(self, chunk_file_path, take_it_slow=False):
        self.chunk_file_path = chunk_file_path
        self.chunk_file_name = get_filename_from_path(self.chunk_file_path)
        self.ELASPIC_TARGET_URL = ELASPIC_MANY_URL
        self.run_mode = None
        self.driver = None
        self.chunk = Chunk()
        if take_it_slow:
            self.DEBUG_DELAY = 5
        log.info('= = = = = = = = = = = = = = = = = = = = = =')
        log.info("STARTING MyScraper ..")
        log.info(f"FILENAME: {self.chunk_file_name} ")
        self.set_run_mode()
        self.run()

    def set_run_mode(self):
        record_response, chunk = get_chunk_record_status(self.chunk_file_path, RECORDS_FOLDER_PATH)
        log.info("RECORD STATUS: {}".format(record_response))
        self.run_mode = record_response
        self.chunk = chunk

    def _initialize_driver(self):
        self.driver = initialize_driver()

    def open_recorded_page(self):
        self.driver.get(self.chunk.elaspic_url)
        # log.info("Webpage Title: {}".format(self.driver.title))

    def open_default_page(self):
        self.driver.get(self.ELASPIC_TARGET_URL)
        # log.info("Webpage Title: {}".format(self.driver.title))

    def run(self):
        # log.info(f"Processing {self.chunk_file_path}")

        if self.run_mode == RecordStatuses.RECORDED_NOT_DOWNLOADED:
            self._initialize_driver()
            # record = Record(RECORDS_FOLDER_PATH, Chunk(file_path=self.chunk_file_path))
            # record.record()
            chunk = self.chunk
            self.open_recorded_page()

        elif self.run_mode == RecordStatuses.NOT_RECORDED:
            self._initialize_driver()
            log.debug('uploading first time.')
            self.open_default_page()
            wait(self.DEBUG_DELAY)  # ------------------------------------------------
            upload_file(self.driver, self.chunk_file_path)

            wait(5)  # ------------------------------------------------
            if not uploaded(self.driver, self.chunk_file_name):
                log.warning('Could not upload the file. skipping..')
                record_upload_failed(self.chunk_file_name)
                self.driver.quit()
                return

            # Wait until all inputs are recognized.
            correctly_input_mutations_flag = process_input_recognization(self.driver)
            chunk = make_chunk(self.driver, file_path=self.chunk_file_path,
                               correctly_input_mutations_flag=correctly_input_mutations_flag)

            # wait(self.DEBUG_DELAY)

            # Click on submit
            wait(self.DEBUG_DELAY)  # ------------------------------------------------
            self.driver.find_element_by_id('submit').click()
            log.info('Clicking SUBMIT button ..')

        elif self.run_mode == RecordStatuses.RECORDED_DOWNLOADED:
            if is_file_located(self.chunk_file_name):
                log.info('file is located! doing nothing..')
                return
            else:
                log.info('Record says file is downloaded, but I could not find it.')
                log.info('Re-downloading from recorded URL.')
                self._initialize_driver()
                chunk = self.chunk
                self.open_recorded_page()

        else:
            print(self.run_mode)
            raise ValueError('run mode not defined properly.')

        # Get current URL.
        chunk.set_url(self.driver.current_url)
        chunk.set_uploaded_status(True)

        log.info("current_url: {}".format(self.driver.current_url))

        wait(self.DEBUG_DELAY)  # ------------------------------------------------

        response = page_computation(self.driver)
        if response == ResponseMessages.COMPLETED:
            # download the allresult file.
            download_result_file(self.driver, TEMP_DOWNLOAD_FOLDER_PATH)
            # move downloaded file to folder where it belongs and organize naming etc.
            organize(TEMP_DOWNLOAD_FOLDER_PATH, self.chunk_file_path, downloaded_filename='allresults.txt')
            chunk.set_downloaded_status(True)
            log.debug(f'+ chunk_downloaded_status : {chunk.downloaded_status}')
            chunk.set_mutations_post_info(get_post_info(self.driver))
            log.info('File is downloaded successfully.')
            # todo run checker code.

        elif response == ResponseMessages.STILL_PROCESSING:
            log.info('Mutations are in process.')
            chunk.set_downloaded_status(False)

        # chunk.print_info()
        record = Record(RECORDS_FOLDER_PATH, chunk)
        record.record()

        wait(self.DEBUG_DELAY * 2)  # ------------------------------------------------

        self.driver.quit()
        # log.info(f"PROCESS COMPLETED FOR {self.chunk_file_path}")
        # log.info('= = = = = = = = = = = = = = = = = = = = = =')


def run_multiple_files(multiple_files):
    for file_path in multiple_files:
        myscapper = MyScraper(file_path, take_it_slow=False)
        wait(0.2)


if __name__ == '__main__':

    TEST_FILES_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\test_files\OV_10_test\*"

    upload_test_file_paths = get_subchunk_files(chunk_path=INPUT_FILES_PATH)

    # print(upload_test_file_paths)
    #
    # ################## RUN OPTION, how many files you want to run?

    upload_test_file_paths_run = upload_test_file_paths[:1]
    #
    while True:
        run_multiple_files(upload_test_file_paths_run)
        log.debug('<END>')
        wait(60, 'cooling down the engines..')
