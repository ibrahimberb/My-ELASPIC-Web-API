from selenium import webdriver
from config import DRIVER_PATH, ELASPIC_MANY_URL

profile = webdriver.FirefoxProfile()
options = webdriver.FirefoxOptions()
# options.headless = HEADLESS


# Set the driver
driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH, firefox_profile=profile)
driver.set_window_position(1024, 0)
driver.set_window_size(1920 - 1024, 1040)

driver.get(ELASPIC_MANY_URL)

##########################
# try:
#     download_result_file(self.driver, TEMP_DOWNLOAD_FOLDER_PATH)
#     organize(TEMP_DOWNLOAD_FOLDER_PATH, self.chunk_file_path, downloaded_filename='allresults.txt')
#     chunk.set_downloaded_status(True)
#     log.debug(f'+ chunk_downloaded_status : {chunk.downloaded_status}')
#     log.info('File is downloaded successfully.')
#
# # Allresults are done, but download clickable object is not visible.
# except ElaspicTimeoutError:
#     log.warning('[WARNING] `download allresults` item not loaded within allowed time.')
#     log.warning('Skipping ..')
#     return