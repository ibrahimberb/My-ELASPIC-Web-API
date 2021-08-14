import logging
from driver_conf import initialize_driver
from selenium.webdriver.support.ui import Select
from interact_page import get_post_info

logging.basicConfig(level=logging.INFO, format='%(message)s')

ELASPIC_TARGET_URL = "http://elaspic.kimlab.org/result/c705b7d6/"

driver = initialize_driver()
driver.get(ELASPIC_TARGET_URL)
logging.info("Webpage Title: {}".format(driver.title))

if __name__ == '__main__':
    get_post_info(driver)
