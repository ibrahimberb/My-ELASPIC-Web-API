# -*- coding: UTF-8 -*-

# Imports
import logging

from upload_utils import upload_file
from utils import make_chunk, get_filename_from_path
from organizer import organize
from config import UPLOAD_FILE_PATH, DOWNLOAD_FOLDER_PATH, RECORDS_FOLDER_PATH
from download_utils import download_result_file
from driver_conf import initialize_driver
from record import has_recorded, Record
import sys

from page_utils import page_computation, ResponseMessages, process_input_recognization

## TODO load csv file and make sure this chunk is not uploaded to ELASPIC before.
#   If it is uploaded, then do not upload again.

# logging.basicConfig(level=logging.INFO, format='%(message)s')
# logging.basicConfig(filename='app.log', level=logging.INFO, format='%(levelname)s:%(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

logging.info(f"Processing {UPLOAD_FILE_PATH}")

chunk_record_flag = has_recorded(UPLOAD_FILE_PATH, "Records_Test")
logging.info("HAS RECORDED: {}".format(chunk_record_flag))
if chunk_record_flag:
    sys.exit("It appears that we already have downloaded this file.\nAborting..")

driver = initialize_driver()
driver.get('http://elaspic.kimlab.org/many/')
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
    logging.info('Operation is completed successfully.')
    # todo run checker code.

elif response == ResponseMessages.STILL_PROCESSING:
    logging.info('Mutations are in proces.')
    chunk.set_downloaded_status(False)

## save the meta info about each subchunk.

print('=======================================================')
print('=======================================================')
chunk.print_info()
print('=======================================================')
record = Record(RECORDS_FOLDER_PATH, chunk)
record.record()
