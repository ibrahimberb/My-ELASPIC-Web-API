# -*- coding: UTF-8 -*-

# Imports
import logging
import traceback
from utils.notify import notify_error
from utils.upload_utils import upload_file
from utils.organizer import organize, is_file_located
from config import (
    TEMP_DOWNLOAD_FOLDER_PATH,
    RECORDS_FOLDER_PATH,
    ELASPIC_MANY_URL,
    INPUT_FILES_PATH,
    ELASPIC_NUM_PARALLEL_COMPUTATION,
    ALLOWED_ATTEMPTS,
)
from utils.download_utils import download_result_file
from utils.driver_conf import initialize_driver
from record import get_chunk_record_status, Record, RecordStatuses
from utils.interact_page import get_post_info, uploaded
from utils.utils import (
    get_filename_from_path,
    wait,
    record_upload_failed,
    record_unexpected_failed,
    get_subchunk_files,
    get_current_time,
    read_chunks_to_run
)
from utils.page_utils import (
    page_computation,
    ResponseMessages,
    process_input_recognization,
    ElaspicTimeoutError,
)
from utils.record_utils import record_allmutations_failed
from chunk import Chunk, make_chunk
from log_script import ColorHandler
from utils.computation_utils import (
    handle_memory_utilization,
    terminate_firefox_processes,
)
from typing import NamedTuple

log = logging.Logger("debug_runner", level=logging.DEBUG)
log.addHandler(ColorHandler())


class RunMode(NamedTuple):
    FAST = 2
    SLOW = 1


class MyScraper:
    DEBUG_DELAY = 0

    def __init__(self, chunk_file_path, run_mode=None):
        self.chunk_file_path = chunk_file_path
        self.chunk_file_name = get_filename_from_path(self.chunk_file_path)
        self.ELASPIC_TARGET_URL = ELASPIC_MANY_URL
        self.run_mode = None
        self.driver = None
        self.num_active_computations = None
        self.chunk = Chunk()
        if run_mode == RunMode.SLOW:
            self.DEBUG_DELAY = 15
        log.info("------------------------------------------------------")
        log.info(f"STARTING MyScraper .. [{get_current_time()}]")
        log.info(f"FILENAME: {self.chunk_file_name} ")
        self.set_run_mode()
        self.run()

    def set_run_mode(self):
        record_response, chunk, num_active_computations = get_chunk_record_status(
            self.chunk_file_path, RECORDS_FOLDER_PATH
        )
        log.info("RECORD STATUS: {}".format(record_response))
        self.run_mode = record_response
        self.chunk = chunk
        self.num_active_computations = int(num_active_computations)

    def _initialize_driver(self):
        self.driver = initialize_driver()

    # PATCH
    # def open_recorded_page(self):
    #     open_page(self.driver, self.chunk.elaspic_url)
    #     # log.info("Webpage Title: {}".format(self.driver.title))
    #
    # def open_default_page(self):
    #     open_page(self.driver, self.ELASPIC_TARGET_URL)
    #     # log.info("Webpage Title: {}".format(self.driver.title))

    # original openers.
    def open_recorded_page(self):
        self.driver.get(self.chunk.elaspic_url)
        # log.info("Webpage Title: {}".format(self.driver.title))

    def open_default_page(self):
        # TODO: handle selenium.common.exceptions.WebDriverException:
        #  Message: Reached error page:
        #  about:neterror?e=netReset&u=http%3A//elaspic.kimlab.org/many/&c=UTF-8&d=The%20connection%20to%20the%20server%20was%20reset%20while%20the%20page%20was%20loading.
        #  Maybe allowed time 3 seconds, repeated attempt.
        self.driver.get(self.ELASPIC_TARGET_URL)
        # log.info("Webpage Title: {}".format(self.driver.title))

    def handle_allmutations_error(self, new_chunk):
        # new_chunk because it now stores post info.
        if self.chunk is None:
            log.critical("UNEXPECTED ERROR: chunk is None and has no attribute 'elaspic_url' "
                         "\nSKIPPING..")
            return

        log.warning("[WARNING] Allresult file is empty. we do not download it.")
        record_allmutations_failed(self.chunk_file_name, self.chunk.elaspic_url)
        record = Record(RECORDS_FOLDER_PATH, new_chunk)
        record.delete_chunk_from_record()

    # todo handle_allmutations_not_reachable
    # def handle_allmutations_not_reachable(self, new_chunk):
    #     # new_chunk because it now handles 'allresults are done' page.
    #     log.warning('[WARNING] Allresult download clickable object not reachable, skipping ..')
    #     return

    def run(self):
        # log.info(f"Processing {self.chunk_file_path}")

        # Ensuring we have available resources.
        handle_memory_utilization()

        if self.run_mode == RecordStatuses.RECORDED_NOT_DOWNLOADED:
            self._initialize_driver()
            chunk = self.chunk

            # URL was stuck to default (elaspic/many), without job code.
            if self.chunk.elaspic_url == ELASPIC_MANY_URL:
                log.warning("[WARNING] URL was stuck, now fixed.")
                record = Record(RECORDS_FOLDER_PATH, chunk)
                record.delete_chunk_from_record()
                log.info("Skipping ..")
                return

            self.open_recorded_page()

        elif self.run_mode == RecordStatuses.NOT_RECORDED:
            log.debug("uploading first time.")
            # todo make it function
            if self.num_active_computations >= ELASPIC_NUM_PARALLEL_COMPUTATION:
                log.warning(
                    f"Number of active computation: {self.num_active_computations}\nAborting Scraper."
                )
                return

            self._initialize_driver()

            self.open_default_page()
            wait(self.DEBUG_DELAY)  # ------------------------------------------------
            upload_file(self.driver, self.chunk_file_path)

            wait(5)  # ------------------------------------------------
            if not uploaded(self.driver, self.chunk_file_name):
                log.warning("Could not upload the file. skipping..")
                record_upload_failed(filename=self.chunk_file_name)
                self.driver.quit()
                return

            # Wait until all inputs are recognized.
            correctly_input_mutations_flag = process_input_recognization(self.driver)
            chunk = make_chunk(
                self.driver,
                file_path=self.chunk_file_path,
                correctly_input_mutations_flag=correctly_input_mutations_flag,
            )

            # Click on submit
            wait(self.DEBUG_DELAY)  # ------------------------------------------------
            self.driver.find_element_by_id("submit").click()
            log.info("Submitting ..")

        elif self.run_mode == RecordStatuses.RECORDED_DOWNLOADED:
            if is_file_located(self.chunk_file_name):
                log.info("file is located! doing nothing..")
                return
            else:
                log.info("Record says file is downloaded, but I could not find it.")
                log.info("Re-downloading from recorded URL.")
                self._initialize_driver()
                chunk = self.chunk
                self.open_recorded_page()

        else:
            print(self.run_mode)
            raise ValueError("run mode not defined properly.")

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
                self.driver.quit()
                return

            try:
                download_result_file(self.driver, TEMP_DOWNLOAD_FOLDER_PATH)
                organize(
                    TEMP_DOWNLOAD_FOLDER_PATH,
                    self.chunk_file_path,
                    downloaded_filename="allresults.txt",
                )
                chunk.set_downloaded_status(True)
                log.debug(f"+ chunk_downloaded_status : {chunk.downloaded_status}")
                log.info("File is downloaded successfully.")

            # Allresults are done, but download clickable object is not visible.
            except ElaspicTimeoutError:
                log.warning(
                    "[WARNING] `download allresults` item not loaded within allowed time."
                )
                log.warning("Skipping ..")
                return

        elif response == ResponseMessages.STILL_PROCESSING:
            log.info("Mutations are in process.")
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


def log_run_options(
        tcga,
        chunks_to_run,
        run_speed,
        chunks_cool_down,
        repeat_chunk_cool_down,
        num_chunk_repeat,
        num_cycles,
        cool_down_cycle,
):
    log.debug("+------------------------+")
    log.debug(f"tcga: {tcga}")
    log.debug(f"chunks_to_run: {chunks_to_run}")
    log.debug(f"run_speed: {run_speed}")
    log.debug(f"chunks_cool_down: {chunks_cool_down}")
    log.debug(f"repeat_chunk_cool_down: {repeat_chunk_cool_down}")
    log.debug(f"num_chunk_repeat: {num_chunk_repeat}")
    log.debug(f"num_cycles: {num_cycles}")
    log.debug(f"cool_down_cycle: {cool_down_cycle}")
    log.debug(f"ELASPIC_NUM_PARALLEL_COMPUTATION: {ELASPIC_NUM_PARALLEL_COMPUTATION}")
    log.debug("+------------------------+")


def run_single_chunk(subchunk_files, run_speed, repeat_cool_down, num_chunk_repeat=1):
    for i in range(num_chunk_repeat):
        log.debug(f"\tREPEAT #{i + 1}")
        for subchunk_file in subchunk_files:
            log.debug(f"\tRUNNING SUB-CHUNK: {subchunk_file} ")
            MyScraper(subchunk_file, run_mode=run_speed)
            wait(0.1)
        log.debug("\t- - - ")
        wait(repeat_cool_down * 60, "[REPEAT CHUNK COOL DOWN]")


def run_multiple_chunks(
        input_path,
        tcga,
        chunks_to_run,
        run_speed,
        cool_down_btw_chunks,
        repeat_chunk_cool_down,
        num_chunk_repeat,
        num_cycles,
        cool_down_cycle,
):
    log_run_options(
        tcga,
        chunks_to_run,
        run_speed,
        cool_down_btw_chunks,
        repeat_chunk_cool_down,
        num_chunk_repeat,
        num_cycles,
        cool_down_cycle,
    )

    for cycle in range(num_cycles):
        log.debug(f"CYCLE: {cycle + 1} OF {num_cycles}")
        for chunk_no in chunks_to_run:
            # Returns 100 chunk files for 1 chunk.
            subchunk_file_paths = get_subchunk_files(
                subchunks_path=input_path, tcga=tcga, chunk_no=chunk_no
            )
            log.debug(
                f" RUNNING {tcga} CHUNK_{chunk_no} ({len(subchunk_file_paths)} subchunk files)"
            )
            log.debug("===========================================================")
            run_single_chunk(
                subchunk_file_paths, run_speed, repeat_chunk_cool_down, num_chunk_repeat
            )
            terminate_firefox_processes()
            wait(cool_down_btw_chunks * 60, "[COOL DOWN BEFORE MOVING ON NEXT CHUNK.]")
        wait(cool_down_cycle * 60, f"[RECHARGING .. ({cool_down_cycle} mins)]")
    log.debug("<END>")


# BRCA
# TCGA = "BRCA"
# CHUNKS_TO_RUN = read_chunks_to_run(TCGA)
# CHUNKS_TO_RUN = [4, 53, 54, 58]

# OV
TCGA = "OV"
CHUNKS_TO_RUN = read_chunks_to_run(TCGA)
# CHUNKS_TO_RUN = [26, 27, 29, 30, 31, 34, 35, 36, 37]


# COAD
# TCGA = 'COAD'
# CHUNKS_TO_RUN = read_chunks_to_run(TCGA)
# CHUNKS_TO_RUN = list(range(1, 128))  # list(range(1, 128))
# EXCLUDED = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 29, 30, 31, 36, 44, 57, 58, 59, 112, 113, 114, 115]
# CHUNKS_TO_RUN = [e for e in CHUNKS_TO_RUN if e not in EXCLUDED]

if __name__ == "__main__":
    fail_count = 0
    while fail_count < ALLOWED_ATTEMPTS:
        try:
            # TEST_FILES_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\test_files\input_files_test"

            run_multiple_chunks(
                INPUT_FILES_PATH,
                tcga=TCGA,
                chunks_to_run=CHUNKS_TO_RUN,
                run_speed=RunMode.FAST,
                cool_down_btw_chunks=0.5,  # 0.3
                repeat_chunk_cool_down=0.1,
                num_chunk_repeat=1,
                num_cycles=15,
                cool_down_cycle=60 * 3,  # 60
            )

            # debug_file = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\ELASPIC_Input\BRCA\4\SNV_BRCA_Chunk_4_82.txt"
            # MyScraper(debug_file, run_mode=RunMode.FAST)
            # exit()

        except Exception as e:
            if "Reached error page" in str(e):
                log.error("=== NETWORK ERROR, TRYING AGAIN .. ===")
                notify_error("network-error-trying")
                wait(15 * 60)
                fail_count += 1
            else:
                log.error("=== UNEXPECTED ERROR ===")  # break?
                print(traceback.format_exc())
                notify_error("unexpected-error", repeat_inf=True)

    log.error("=== UNEXPECTED ERROR ===")
    notify_error("unexpected-error", repeat_inf=True)
