from selenium.common.exceptions import NoSuchElementException
import logging
from selenium.webdriver.support.ui import Select

logging.basicConfig(level=logging.INFO, format='%(message)s')

PAGE_POST_STATUSES = ['done', 'error', 'running']


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
