# -*- coding: UTF-8 -*-

# Imports
import logging

from utils.upload_utils import upload_file
from utils.organizer import organize, is_file_located
from config import TEMP_DOWNLOAD_FOLDER_PATH, RECORDS_FOLDER_PATH, ELASPIC_MANY_URL, INPUT_FILES_PATH, \
    ELASPIC_NUM_PARALLEL_COMPUTATION
from utils.download_utils import download_result_file
from utils.driver_conf import initialize_driver
from record import get_chunk_record_status, Record, RecordStatuses
from utils.interact_page import get_post_info, uploaded
from utils.utils import get_filename_from_path, wait, record_upload_failed, record_unexpected_failed, \
    get_subchunk_files
from utils.page_utils import page_computation, ResponseMessages, process_input_recognization
from utils.record_utils import record_allmutations_failed
from chunk import Chunk, make_chunk
from log_script import ColorHandler

log = logging.Logger('debug_runner', level=logging.DEBUG)
log.addHandler(ColorHandler())


class RunMode:
    FAST = False
    SLOW = True


class MyScraper:
    DEBUG_DELAY = 0

    def __init__(self, chunk_file_path, take_it_slow=False):
        self.chunk_file_path = chunk_file_path
        self.chunk_file_name = get_filename_from_path(self.chunk_file_path)
        self.ELASPIC_TARGET_URL = ELASPIC_MANY_URL
        self.run_mode = None
        self.driver = None
        self.num_active_computations = None
        self.chunk = Chunk()
        if take_it_slow:
            self.DEBUG_DELAY = 15
        log.info('------------------------------------------------------')
        log.info("STARTING MyScraper ..")
        log.info(f"FILENAME: {self.chunk_file_name} ")
        self.set_run_mode()
        self.run()

    def set_run_mode(self):
        record_response, chunk, num_active_computations = get_chunk_record_status(self.chunk_file_path,
                                                                                  RECORDS_FOLDER_PATH)
        log.info("RECORD STATUS: {}".format(record_response))
        self.run_mode = record_response
        self.chunk = chunk
        self.num_active_computations = int(num_active_computations)

    def _initialize_driver(self):
        self.driver = initialize_driver()

    def open_recorded_page(self):
        self.driver.get(self.chunk.elaspic_url)
        # log.info("Webpage Title: {}".format(self.driver.title))

    def open_default_page(self):
        self.driver.get(self.ELASPIC_TARGET_URL)
        # log.info("Webpage Title: {}".format(self.driver.title))

    def handle_allmutations_error(self, new_chunk):
        # new_chunk because it now stores post info.
        log.warning('Allresult file is empty. we do not download it.')
        record_allmutations_failed(self.chunk_file_name, self.chunk.elaspic_url)
        record = Record(RECORDS_FOLDER_PATH, new_chunk)
        record.delete_chunk_from_record()

    def run(self):
        # log.info(f"Processing {self.chunk_file_path}")

        if self.run_mode == RecordStatuses.RECORDED_NOT_DOWNLOADED:
            self._initialize_driver()
            # record = Record(RECORDS_FOLDER_PATH, Chunk(file_path=self.chunk_file_path))
            # record.record()
            chunk = self.chunk
            self.open_recorded_page()

        elif self.run_mode == RecordStatuses.NOT_RECORDED:
            log.debug('uploading first time.')
            # todo make it function
            if self.num_active_computations >= ELASPIC_NUM_PARALLEL_COMPUTATION:
                log.warning(
                    f"Number of active computation: {self.num_active_computations}\nAborting Scraper.")
                return

            self._initialize_driver()

            self.open_default_page()
            wait(self.DEBUG_DELAY)  # ------------------------------------------------
            upload_file(self.driver, self.chunk_file_path)

            wait(5)  # ------------------------------------------------
            if not uploaded(self.driver, self.chunk_file_name):
                log.warning('Could not upload the file. skipping..')
                record_upload_failed(filename=self.chunk_file_name)
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
            log.info('Submitting ..')

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
            chunk.set_mutations_post_info(get_post_info(self.driver))

            # This means the webpage ERR for all inputs.
            if chunk.num_mutations_done == 0:
                self.handle_allmutations_error(chunk)
                return

            download_result_file(self.driver, TEMP_DOWNLOAD_FOLDER_PATH)
            organize(TEMP_DOWNLOAD_FOLDER_PATH, self.chunk_file_path, downloaded_filename='allresults.txt')
            chunk.set_downloaded_status(True)
            log.debug(f'+ chunk_downloaded_status : {chunk.downloaded_status}')
            log.info('File is downloaded successfully.')

        elif response == ResponseMessages.STILL_PROCESSING:
            log.info('Mutations are in process.')
            chunk.set_downloaded_status(False)

        elif response == ResponseMessages.RESULT_PAGE_NOT_LOADED:
            log.warning("[WARNING] RESULT_PAGE_NOT_LOADED")
            record_unexpected_failed(filename=self.chunk_file_name)
            self.driver.quit()
            return

        record = Record(RECORDS_FOLDER_PATH, chunk)
        record.record()

        wait(self.DEBUG_DELAY)  # ------------------------------------------------

        self.driver.quit()


def run_single_chunk(subchunk_files, run_speed, num_repeat=3):
    for i in range(num_repeat):
        log.debug(f"\tREPEAT #{i + 1}")
        for subchunk_file in subchunk_files:
            log.debug(f"\tRUNNING SUB-CHUNK: {subchunk_file} ")
            myscapper = MyScraper(subchunk_file, take_it_slow=run_speed)
            wait(0.1)
        log.debug('\t- - - ')
        wait(10, '[REPEAT COOL DOWN]')


def run_multiple_chunks(input_path, tcga, chunks_to_run, run_speed):
    for chunk_no in chunks_to_run:
        # Returns 100 chunk files for 1 chunk.
        subchunk_file_paths = get_subchunk_files(subchunks_path=input_path, tcga=tcga, chunk_no=chunk_no)
        log.debug(f' RUNNING {tcga} CHUNK_{chunk_no} ({len(subchunk_file_paths)} subchunk files)')
        log.debug('===========================================================')
        run_single_chunk(subchunk_file_paths, run_speed)
        wait(60, 'cooling down the engines..')
    log.debug('<END>')


if __name__ == '__main__':
    # TEST_FILES_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\test_files\input_files_test"

    TCGA = 'OV'
    # list(range(2, 6))
    run_multiple_chunks(INPUT_FILES_PATH, tcga=TCGA, chunks_to_run=[3], run_speed=RunMode.FAST)
