# -*- coding: UTF-8 -*-

# Imports
import logging

from upload_utils import upload_file
from utils import make_chunk
from organizer import organize
from config import DOWNLOAD_FOLDER_PATH, RECORDS_FOLDER_PATH, ELASPIC_MANY_URL
from download_utils import download_result_file
from driver_conf import initialize_driver
from record import get_chunk_record_status, Record, RecordStatuses
from interact_page import get_post_info, PAGE_POST_STATUSES
from page_utils import page_computation, ResponseMessages, process_input_recognization
from chunk import Chunk
from utils import wait

logging.basicConfig(level=logging.INFO, format='[MyScapper] %(message)s')


class MyScraper:
    DEBUG_DELAY = 0

    def __init__(self, chunk_file_path, take_it_slow=False):
        logging.info("STARTING MyScraper ..")
        logging.info(f"FILEPATH: {chunk_file_path} ")
        self.chunk_file_path = chunk_file_path
        self.ELASPIC_TARGET_URL = ELASPIC_MANY_URL
        self.run_mode = None
        self.driver = None
        if take_it_slow:
            self.DEBUG_DELAY = 5
        self.run()

    def set_run_mode(self):
        record_response, new_url = get_chunk_record_status(self.chunk_file_path, "Records_Test")
        logging.info("HAS RECORDED: {}".format(record_response))
        if record_response == RecordStatuses.RECORDED_DOWNLOADED:
            self.run_mode = RecordStatuses.RECORDED_DOWNLOADED
            # sys.exit("It appears that we already have downloaded this file.\nAborting..")
            return

        elif record_response == RecordStatuses.RECORDED_NOT_DOWNLOADED:
            self.run_mode = RecordStatuses.RECORDED_NOT_DOWNLOADED
            logging.info('target url is changed.')
            self.ELASPIC_TARGET_URL = new_url

        elif record_response == RecordStatuses.NOT_RECORDED:
            logging.info('uploading first time.')
            self.run_mode = RecordStatuses.NOT_RECORDED

    def prepare_browser(self):
        self.driver = initialize_driver()
        self.driver.get(self.ELASPIC_TARGET_URL)
        logging.info("Webpage Title: {}".format(self.driver.title))

    def run(self):
        self.set_run_mode()
        self.prepare_browser()
        logging.info(f"Processing {self.chunk_file_path}")

        if self.run_mode == RecordStatuses.RECORDED_DOWNLOADED:
            return

        elif self.run_mode == RecordStatuses.RECORDED_NOT_DOWNLOADED:
            chunk = Chunk(self.chunk_file_path)

        elif self.run_mode == RecordStatuses.NOT_RECORDED:
            # Upload the file.
            upload_file(self.driver, self.chunk_file_path)
            # Wait until all inputs are recognized.
            correctly_input_mutations_flag = process_input_recognization(self.driver)
            # make a chunk object.
            chunk = make_chunk(self.driver, file_path=self.chunk_file_path,
                               correctly_input_mutations_flag=correctly_input_mutations_flag)

            # Click on submit
            self.driver.find_element_by_id('submit').click()
            logging.info('Clicking SUBMIT button ..')

            # Get current URL.
            chunk.set_url(self.driver.current_url)
            chunk.set_uploaded_status(True)

        else:
            print(self.run_mode)
            raise ValueError('run mode not defined properly.')

        wait(self.DEBUG_DELAY)  # ------------------------------------------------

        logging.info("current_url: {}".format(self.driver.current_url))

        wait(self.DEBUG_DELAY)  # ------------------------------------------------

        response = page_computation(self.driver)
        if response == ResponseMessages.COMPLETED:
            # download the allresult file.
            download_result_file(self.driver, DOWNLOAD_FOLDER_PATH)
            # move downloaded file to folder where it belongs and organize naming etc.
            organize(DOWNLOAD_FOLDER_PATH, self.chunk_file_path, downloaded_filename='allresults.txt')
            chunk.set_downloaded_status(True)
            # chunk.set_mutations_post_info(get_post_info(self.driver, 'error'))
            chunk.set_mutations_post_info(get_post_info(self.driver))
            logging.info('File is downloaded successfully.')
            # todo run checker code.

        elif response == ResponseMessages.STILL_PROCESSING:
            logging.info('Mutations are in proces.')
            chunk.set_downloaded_status(False)

        wait(self.DEBUG_DELAY * 2)  # ------------------------------------------------

        # chunk.print_info()
        record = Record(RECORDS_FOLDER_PATH, chunk)
        record.record()

        chunk.print_info()
        self.driver.quit()
        logging.info(f"PROCESS COMPLETED FOR {self.chunk_file_path}")
        logging.info('= = = = = = = = =')


if __name__ == '__main__':
    import glob
    from itertools import cycle

    TEST_FILES_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\BRCA_10_test\*"

    upload_test_file_paths = [file for file in
                              glob.glob(TEST_FILES_PATH)
                              if 'Chunk_22' in file]

    upload_test_file_paths = upload_test_file_paths[:1]

    # upload_test_file_paths = [file for file in
    #                           glob.glob(TEST_FILES_PATH)
    #                           if 'SNV_BRCA_Chunk_22_21.txt' in file]

    upload_test_file_paths_cycle = cycle(upload_test_file_paths)
    for file_path in upload_test_file_paths_cycle:
        myscapper = MyScraper(file_path)
        break

    print('<END>')
