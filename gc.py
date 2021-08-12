# def process_single_error(html_text):
#
#     invalid_syntax = None
#     num_invalid_syntax = None
#     unrecognized_gene_symbols = None
#     num_unrecognized_gene_symbols = None
#     unrecognized_protein_residues = None
#     num_unrecognized_protein_residues = None
#     duplicates = None
#     num_duplicates = None
#     outside_of_structural_domain = None
#     num_outside_of_structural_domain = None
#
#     soup_single_error = BS(html_text, 'lxml')
#
#     soup_copy = soup_single_error.__copy__()
#
#     for s in soup_copy.select('span'):
#         s.extract()
#
#     print(' TITLE '.center(40, '-'))
#     print('TITLE:', soup_copy.get_text())
#
#     error_items = soup_single_error.find("span", {"class": "resp"})
#
#     print("VALUES:")
#     values = [value.strip() for value in error_items.get_text().split(',')]
#     print(values)

wait_being_processed = WebDriverWait(driver, 3)  # PROCESS_TIMEOUT minutes
try:
    # If "All the mutations are done!" not shown, find processing.
    if not EC.visibility_of_element_located((By.XPATH, '//*[@id="summary"]/div[2]/div[1]')):
        wait_results_page_load.until(EC.visibility_of_element_located((By.ID, 'notreadyyet')))

except TimeoutException:
    raise TimeoutException("could not find `all the mutations are done!` or `mutations being processed` texts.")