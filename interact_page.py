from selenium.common.exceptions import NoSuchElementException
import logging
from driver_conf import initialize_driver
from selenium.webdriver.support.ui import Select

logging.basicConfig(level=logging.INFO, format='%(message)s')

STATUS_TYPES = ['done', 'error']


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


def get_post_info(driver, status_type):
    assert status_type in STATUS_TYPES

    info_prot_mut_pairs = []

    select = Select(driver.find_element_by_class_name('pagesize'))
    select.select_by_value('all')
    table_id = driver.find_element_by_id('resulttable')
    rows = table_id.find_elements_by_tag_name("tr")[1:]

    for row in rows:
        protein_mutation = row.get_attribute('data-pnt')

        attr = row.get_attribute("class").split(' ')[0]

        if attr == status_type:
            info_prot_mut_pairs.append(protein_mutation)

        print(f"{protein_mutation} \t {attr}")

    post_info = {'elements': info_prot_mut_pairs,
                 'num_elements': len(info_prot_mut_pairs)}

    print('ELEMENTS: {}'.format(post_info['elements']))
    print('NUM_ELEMENTS: {}'.format(post_info['num_elements']))
    print('= = = = = = = = = = = = = = = = = = ')
    return post_info
