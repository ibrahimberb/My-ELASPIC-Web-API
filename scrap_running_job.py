# -*- coding: UTF-8 -*-
# Imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
from interact_page import check_exists_by_xpath, check_exists_by_id
import time
from page_utils import page_computation

logging.basicConfig(level=logging.INFO, format='%(message)s')

# Paths
DRIVER_PATH = r"C:\webdrivers\geckodriver.exe"

# Set the Options.
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
# profile.set_preference("browser.download.dir", str(DOWNLOAD_FOLDER_PATH))
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')  # type of file to download

# Set the driver
driver = webdriver.Firefox(executable_path=DRIVER_PATH, firefox_profile=profile)
driver.set_window_position(1024, 0)
driver.set_window_size(1920 - 1024, 1040)

driver.get('http://elaspic.kimlab.org/result/c3e206aa/')  # processing
# driver.get('http://elaspic.kimlab.org/result/7585c335/')  # done
logging.info("My ELASPIC API starts for processing job ..")
logging.info("Webpage Title: {}".format(driver.title))

wait_processing = WebDriverWait(driver, 60 * 10)  # 10 minutes

# wait_processing.until(EC.visibility_of_element_located((By.ID, 'notreadyyet')))
wait_processing.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="summary"]/div[1]/h2')))
logging.info('page is loaded, either DONE or PROCESSING .. ')

# print(check_exists_by_id('notreadyyet'))
COMPUTATION_TIME_ALLOWED = 0.5

page_computation(driver)
