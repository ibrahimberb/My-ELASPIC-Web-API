from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
import logging
from selenium.webdriver.support.ui import Select
from utils.exceptions import NetworkError
import time

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

PAGE_POST_STATUSES = ['done', 'error', 'running']


# def open_page(driver: WebDriver, elaspic_url, allowed_attempts=3):
#     n_attempts = 0
#     while n_attempts < allowed_attempts:
#         try:
#             driver.get(elaspic_url)
#             break
#         except WebDriverException:
#             print('error !!!')
#             time.sleep(3)
#             n_attempts += 1
#             logging.warning(f'[WARNING] Could not open the webpage, URL: {elaspic_url}')
#             logging.warning(f'\tAttempt {n_attempts}')
#
#     logging.warning(f'current URL: {driver.current_url}')
#     logging.warning(f'[WARNING] page is failed to open.')
#     raise NetworkError


def check_exists_by_id(driver, element_id):
    try:
        driver.find_element_by_id(element_id)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_xpath(driver, element_xpath):
    try:
        driver.find_element_by_xpath(element_xpath)
    except NoSuchElementException:
        return False
    return True


def get_post_info(driver):
    post_info = {f'mutations_{status}': [] for status in PAGE_POST_STATUSES}

    select = Select(driver.find_element_by_class_name('pagesize'))
    select.select_by_value('all')
    table_id = driver.find_element_by_id('resulttable')
    rows = table_id.find_elements_by_tag_name("tr")[1:]

    for row in rows:
        protein_mutation = row.get_attribute('data-pnt').split('_')[0]  # P01116.G12V_13360419 → P01116.G12V

        status = row.get_attribute("class").split(' ')[0]
        post_info[f"mutations_{status}"].append(protein_mutation)
        logging.debug(f"{protein_mutation} \t {status}")

    for status in PAGE_POST_STATUSES:
        post_info[f'num_mutations_{status}'] = len(post_info[f'mutations_{status}'])

    logging.debug('post_info: {}'.format(post_info))
    return post_info


def uploaded(driver, chunk_file_name):
    # upload_err_txt = str(driver.find_element_by_id('uploaderr').text).strip()
    resp_wrapper_txt = str(driver.find_element_by_id('resp_wrapper').text).strip()
    # print('resp_wrapper_txt: *{}*'.format(resp_wrapper_txt))
    resp_wrapper_visible = not bool(resp_wrapper_txt)
    if resp_wrapper_visible:
        return False
    return True
