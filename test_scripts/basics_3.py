# import logging
# from driver_conf import initialize_driver
# from selenium.webdriver.support.ui import Select
#
# logging.basicConfig(level=logging.INFO, format='%(message)s')
#
# # ELASPIC_TARGET_URL = "http://elaspic.kimlab.org/result/22e1d75c/"
# #
# # driver = initialize_driver()
# # driver.get(ELASPIC_TARGET_URL)
# # logging.info("Webpage Title: {}".format(driver.title))
# #
# STATUS_TYPES = ['done', 'error']
#
#
# def get_post_info(driver, status_type):
#     assert status_type in STATUS_TYPES
#
#     info_prot_mut_pairs = []
#
#     select = Select(driver.find_element_by_class_name('pagesize'))
#     select.select_by_value('all')
#     table_id = driver.find_element_by_id('resulttable')
#     rows = table_id.find_elements_by_tag_name("tr")[1:]
#
#     for row in rows:
#         protein_mutation = row.get_attribute('data-pnt')
#         print(f"protein: {protein_mutation}")
#
#         attr = row.get_attribute("class").split(' ')[0]
#
#         print(f"attrs: {attr}")
#
#         if attr == status_type:
#             info_prot_mut_pairs.append(protein_mutation)
#
#         print('- - - - - - - - - - - - - - - - - - ')
#     print('ELEMENTS: {}'.format(info_prot_mut_pairs))
#     print('NUM_ELEMENTS: {}'.format(len(info_prot_mut_pairs)))
#     print('= = = = = = = = = = = = = = = = = = ')
#
#
# if __name__ == '__main__':
#     get_post_info('error')
