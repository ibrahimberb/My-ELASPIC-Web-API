import os
import logging
import inspect

from bs4 import BeautifulSoup as BS
from utils.interact_page import check_exists_by_xpath

from input.scrap_record import process_single_error

logging.basicConfig(level=logging.INFO, format='[INFO] %(message)s')


class Chunk:
    ## a subchunk

    def __init__(self, file_path=None, num_correctly_input_mutations=0,
                 invalid_syntax=None, num_invalid_syntax=0,
                 unrecognized_gene_symbols=None, num_unrecognized_gene_symbols=0,
                 unrecognized_protein_residues=None, num_unrecognized_protein_residues=0,
                 duplicates=None, num_duplicates=0,
                 outside_of_structural_domain=None, num_outside_of_structural_domain=0,
                 elaspic_url=None, uploaded_status=None, downloaded_status=None):
        # path, codes, names
        self.file_path = file_path
        self.tcga_code, self.chunk_no, self.subchunk_no = self.parse_filename()
        self.file_name = self.get_filename_from_path()
        # Num corr. input mutations
        self.num_correctly_input_mutations = int(num_correctly_input_mutations)
        # Errors
        self.invalid_syntax = invalid_syntax
        self.num_invalid_syntax = int(num_invalid_syntax)
        self.unrecognized_gene_symbols = unrecognized_gene_symbols
        self.num_unrecognized_gene_symbols = int(num_unrecognized_gene_symbols)
        self.unrecognized_protein_residues = unrecognized_protein_residues
        self.num_unrecognized_protein_residues = int(num_unrecognized_protein_residues)
        self.duplicates = duplicates
        self.num_duplicates = int(num_duplicates)
        self.outside_of_structural_domain = outside_of_structural_domain
        self.num_outside_of_structural_domain = int(num_outside_of_structural_domain)
        # additional information
        self.elaspic_url = elaspic_url
        self.uploaded_status = uploaded_status
        self.downloaded_status = downloaded_status
        # number of entries uploaded to ELASPIC in input recognition step.
        self.total_num_uploaded_entry = self.num_correctly_input_mutations + self.num_invalid_syntax \
                                        + self.num_unrecognized_gene_symbols \
                                        + self.num_unrecognized_protein_residues + self.num_duplicates \
                                        + self.num_outside_of_structural_domain

        # number of lines in text file.
        self.num_lines = self.get_num_lines()
        # after web page computation - post info
        self.mutations_done = None
        self.num_mutations_done = 0
        self.mutations_error = None
        self.num_mutations_error = 0
        self.mutations_running = None
        self.num_mutations_running = 0

    def get_filename_from_path(self):
        if self.file_path is None:
            return None

        return os.path.basename(self.file_path)

    def set_mutations_post_info(self, post_info_dict):
        logging.debug(f"setting chunk's post info.`")
        self.mutations_done = post_info_dict['mutations_done']
        self.num_mutations_done = post_info_dict['num_mutations_done']
        self.mutations_error = post_info_dict['mutations_error']
        self.num_mutations_error = post_info_dict['num_mutations_error']
        self.mutations_running = post_info_dict['mutations_running']
        self.num_mutations_running = post_info_dict['num_mutations_running']

    def set_url(self, url):
        logging.debug("setting chunk's attr: `ELASPIC_URL`")
        self.elaspic_url = url

    def set_uploaded_status(self, uploaded_status):
        logging.debug("setting chunk's attr:", uploaded_status)
        self.uploaded_status = int(uploaded_status)

    def set_downloaded_status(self, downloaded_status):
        logging.debug("setting chunk's attr:", downloaded_status)
        self.downloaded_status = int(downloaded_status)

    def get_num_lines(self):
        """Returns number of lines in text file."""
        if self.file_path is None:
            return 0

        with open(self.file_path) as chunk_file:
            lines = chunk_file.readlines()
            lines = [line.strip() for line in lines if line.strip() != '']
            return len(lines)

    def parse_filename(self):
        """
        Parses the filepath

        Parameters
        ----------
            filepath :
                Filepath of chunkfile. E.g. SNV_BRCA_Chunk_22_0_test.txt
        Returns
        -------
            tcga_code, chunk_no, subchunk_no
        """
        if self.file_path is None:
            return None, None, None

        # Extract filename from filepath
        filename = os.path.basename(self.file_path)
        filename = filename.replace('.txt', '')
        filename_splitted = filename.split('_')
        tcga_code, chunk_no, subchunk_no = filename_splitted[1], filename_splitted[3], filename_splitted[4]

        return tcga_code, chunk_no, subchunk_no

    def extract_info(self):
        with open(f"{self.chunk_no}_{self.subchunk_no}_info.txt", 'w') as info_file:
            pass

            # info_file.write("num_correctly_input_mutations: {}".format(self.num_correctly_input_mutations))
            # info_file.write("num_invalid_syntax: {}".format(self.num_invalid_syntax))
            # info_file.write("num_unrecognized_gene_symbols: {}".format(self.num_unrecognized_gene_symbols))
            # info_file.write("num_unrecognized_protein_residues: {}".format(self.num_unrecognized_protein_residues))
            # info_file.write("num_duplicates: {}".format(self.num_duplicates))
            # info_file.write("num_outside_of_structural_domain: {}".format(self.num_outside_of_structural_domain))
            # info_file.write("file_path: {}".format(self.file_path))
            # info_file.write("get_num_lines: {}".format(self.get_num_lines()))
            # info_file.write("total_num_entry: {}".format(self.total_num_entry))

    def get_attributes(self):
        return self.__dict__.keys()

    def print_info(self):
        print(" - - - CHUNK INFO - - - ")
        for attr in self.get_attributes():
            print(f" → {attr}: {getattr(self, attr)}")


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

    if check_exists_by_xpath(driver, '//*[@id="input_err"]/div/h4'):
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

    else:
        logging.warning("No error, surprizingly.")

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


def get_chunk_init_args():
    # TODO
    signature = inspect.signature(Chunk.__init__)
    return list(signature.parameters.values())
