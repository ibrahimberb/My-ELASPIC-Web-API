import glob
from MyScraper import MyScraper
import logging
from log_script import ColorHandler

log = logging.Logger('debug_runner', level=logging.DEBUG)
log.addHandler(ColorHandler())

log.info("Starting debugger.")

# TEST_FILES_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\OV_10_test\*"
TEST_FILES_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\*"

upload_test_file_paths = [file for file in
                          glob.glob(TEST_FILES_PATH)
                          if 'SNV_BRCA_Chunk_X_X.txt' in file]

upload_test_file_path = upload_test_file_paths[0]
print("upload_test_file_path:", upload_test_file_path)

MyScraper(upload_test_file_path, run_mode=False)

log.info('<END>')
