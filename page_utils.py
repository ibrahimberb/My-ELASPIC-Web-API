from interact_page import check_exists_by_xpath, check_exists_by_id
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
from selenium.common.exceptions import TimeoutException
from config import COMPUTATION_TIME_ALLOWED

logging.basicConfig(level=logging.INFO, format='%(message)s')


class ResponseMessages:
    STILL_PROCESSING = "STILL_PROCESSING"
    COMPLETED = "COMPLETED"


def click_button_by_xpath(driver, element_xpath):
    click_button_wait = WebDriverWait(driver, 3)
    click_button_wait.until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    driver.find_element_by_xpath(element_xpath).click()


def page_computation(driver):
    wait_results_page_load = WebDriverWait(driver, 10)  # 10 seconds to load
    try:
        wait_results_page_load.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="summary"]/div[1]/h2')))
        if check_exists_by_id(driver, 'notreadyyet'):
            computation_time_elasped_seconds = 0
            job_completed = False
            check_frequency = 5  # check in every 5 seconds.

            # mutations are still being processed.
            print(driver.find_element_by_id('notreadyyet').find_element_by_tag_name('p').text)

            while computation_time_elasped_seconds < (COMPUTATION_TIME_ALLOWED * 60) and not job_completed:
                computation_time_elasped_seconds += check_frequency
                time.sleep(check_frequency)
                if not check_exists_by_id(driver, 'notreadyyet'):
                    logging.info('JOB COMPLETED.')
                    job_completed = True
                else:
                    logging.info(
                        'still not completed. waiting .. [time elapsed: {}]'.format(computation_time_elasped_seconds))

            if not job_completed:
                logging.info("I had enough.. can't wait any longer.")
                return ResponseMessages.STILL_PROCESSING

        elif check_exists_by_xpath(driver, '//*[@id="summary"]/div[2]/div[1]'):
            print(driver.find_element_by_xpath('//*[@id="summary"]/div[2]/div[1]').text)
            return ResponseMessages.COMPLETED

        else:
            raise Exception('Unexpected error.')

    except TimeoutException:
        logging.warning("Result page not loaded!")
        raise TimeoutException('Timeout..')


def process_input_recognization(driver):
    # Wait until all inputs are recognized.
    input_recognition_wait = WebDriverWait(driver, 20)  # 10
    # Waiting for information box to appear.
    try:
        input_recognition_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="input_resp"]/div/h4')))
        correctly_input_mutations_flag = True
    except TimeoutException:
        logging.warning("Could not find any correctly input mutation. Retrieving error mutations ..")
        input_recognition_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="input_err"]')))
        correctly_input_mutations_flag = False

    return correctly_input_mutations_flag
