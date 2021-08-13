# -*- coding: UTF-8 -*-

# Imports
import logging

from upload_utils import upload_file
from utils import make_chunk
from organizer import organize
from config import UPLOAD_FILE_PATH, DOWNLOAD_FOLDER_PATH, RECORDS_FOLDER_PATH, ELASPIC_MANY_URL
from download_utils import download_result_file
from driver_conf import initialize_driver
from record import get_chunk_record_status, Record, RecordStatuses
import sys
from page_utils import page_computation, ResponseMessages, process_input_recognization
from page_utils import click_button_by_id

ELASPIC_TARGET_URL = ELASPIC_MANY_URL

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

logging.info(f"Processing {UPLOAD_FILE_PATH}")

record_response, new_url = get_chunk_record_status(UPLOAD_FILE_PATH, "Records_Test")
logging.info("HAS RECORDED: {}".format(record_response))
if record_response == RecordStatuses.RECORDED_DOWNLOADED:
    sys.exit("It appears that we already have downloaded this file.\nAborting..")
elif record_response == RecordStatuses.RECORDED_NOT_DOWNLOADED:
    logging.info('target url is changed.')
    ELASPIC_TARGET_URL = new_url
elif record_response == RecordStatuses.NOT_RECORDED:
    logging.info('uploading first time.')

driver = initialize_driver()
driver.get(ELASPIC_TARGET_URL)
logging.info("Webpage Title: {}".format(driver.title))

# Upload the file.
upload_file(driver, UPLOAD_FILE_PATH)

# Wait until all inputs are recognized.
correctly_input_mutations_flag = process_input_recognization(driver)

# make a chunk object.
chunk = make_chunk(driver, file_path=UPLOAD_FILE_PATH,
                   correctly_input_mutations_flag=correctly_input_mutations_flag)

chunk.print_info()

print('===========================================================')

# Click on submit
driver.find_element_by_id('submit').click()
logging.info('Clicking SUBMIT button ..')
### replace above lines by
# click_button_by_id(driver, 'submit')
# logging.info('Clicking SUBMIT button ..')

# Get current URL.
logging.info("current_url: {}".format(driver.current_url))
logging.info("setting chunk's URL ..")
chunk.set_url(driver.current_url)
chunk.set_uploaded_status(True)

print('===========================================================')

response = page_computation(driver)
if response == ResponseMessages.COMPLETED:
    # download the allresult file.
    download_result_file(driver, DOWNLOAD_FOLDER_PATH)
    # move downloaded file to folder where it belongs and organize naming etc.
    organize(DOWNLOAD_FOLDER_PATH, UPLOAD_FILE_PATH, downloaded_filename='allresults.txt')
    chunk.set_downloaded_status(True)
    logging.info('File is downloaded successfully.')
    # todo run checker code.

elif response == ResponseMessages.STILL_PROCESSING:
    logging.info('Mutations are in proces.')
    chunk.set_downloaded_status(False)

# chunk.print_info()
print('=======================================================')
record = Record(RECORDS_FOLDER_PATH, chunk)
record.record()

logging.info('WE ARE DONE.')
