from bs4 import BeautifulSoup as BS
from input.scrap_record import process_single_error
import logging
from chunk import Chunk
import os
import time
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(message)s')


# def wait(duration):
#     time_elasped = 0
#     while time_elasped < duration:
#         print('.', end='')
#         time.sleep(0.1)
#         time_elasped += 0.1
#     print()

def wait(duration):
    if duration == 0:
        return
    for _ in tqdm(range(duration), desc='[WAIT_DELAY]', position=0, leave=True):
        time.sleep(1)


def is_valid_file(filepath):
    with open(filepath) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip() != '']

    logging.info('number of lines {}'.format(len(lines)))
    return len(lines) > 0


def get_filename_from_path(filepath):
    filename = os.path.basename(filepath)
    return filename


# todo refactor and introduce another function
def make_chunk(driver, file_path, correctly_input_mutations_flag=True):
    invalid_syntax = None
    num_invalid_syntax = 0
    unrecognized_gene_symbols = None
    num_unrecognized_gene_symbols = 0
    unrecognized_protein_residues = None
    num_unrecognized_protein_residues = 0
    duplicates = None
    num_duplicates = 0
    outside_of_structural_domain = None
    num_outside_of_structural_domain = 0

    if correctly_input_mutations_flag:
        # Find number of correctly input mutations.
        input_resp = driver.find_element_by_xpath('//*[@id="input_resp"]/div/h4')
        num_correctly_input_mutations = int(str(input_resp.text).split()[0])
        logging.info(input_resp.text)
    else:
        num_correctly_input_mutations = 0

    # Find invalid input mutations and their occurrance.
    input_err_str = driver.find_element_by_xpath('//*[@id="input_err"]/div/h4')
    logging.info(input_err_str.text)

    html = driver.page_source

    soup = BS(html, 'lxml')

    # Iterate over error types.
    errors = soup.find("div", {"id": "input_err"})
    for error_type in errors.find_all('p'):
        # print(error_type)
        error_title, values, num_values = process_single_error(str(error_type))

        if error_title == 'Invalid syntax':
            invalid_syntax = values
            num_invalid_syntax = num_values

        elif error_title == 'Unrecognized gene symbols':
            unrecognized_gene_symbols = values
            num_unrecognized_gene_symbols = num_values

        elif error_title == 'Unrecognized protein residues':
            unrecognized_protein_residues = values
            num_unrecognized_protein_residues = num_values

        elif error_title == 'Duplicates':
            duplicates = values
            num_duplicates = num_values

        elif error_title == 'Outside of structural domain':
            outside_of_structural_domain = values
            num_outside_of_structural_domain = num_values

        else:
            raise ValueError("Error Title unexpected!")

    chunk = Chunk(file_path=file_path, num_correctly_input_mutations=num_correctly_input_mutations,
                  invalid_syntax=invalid_syntax, num_invalid_syntax=num_invalid_syntax,
                  unrecognized_gene_symbols=unrecognized_gene_symbols,
                  num_unrecognized_gene_symbols=num_unrecognized_gene_symbols,
                  unrecognized_protein_residues=unrecognized_protein_residues,
                  num_unrecognized_protein_residues=num_unrecognized_protein_residues,
                  duplicates=duplicates, num_duplicates=num_duplicates,
                  outside_of_structural_domain=outside_of_structural_domain,
                  num_outside_of_structural_domain=num_outside_of_structural_domain)

    return chunk
