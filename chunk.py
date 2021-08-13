import os
import logging

logging.basicConfig(level=logging.INFO, format='[CHUNK] %(message)s')


class Chunk:
    ## a subchunk

    def __init__(self, file_path=None, num_correctly_input_mutations=0,
                 invalid_syntax=None, num_invalid_syntax=0,
                 unrecognized_gene_symbols=None, num_unrecognized_gene_symbols=0,
                 unrecognized_protein_residues=None, num_unrecognized_protein_residues=0,
                 duplicates=None, num_duplicates=0,
                 outside_of_structural_domain=None, num_outside_of_structural_domain=0):
        # path, codes, names
        self.file_path = file_path
        self.tcga_code, self.chunk_no, self.subchunk_no = self.parse_filename()
        self.file_name = os.path.basename(self.file_path)
        # Num corr. input mutations
        self.num_correctly_input_mutations = num_correctly_input_mutations
        # Errors
        self.invalid_syntax = invalid_syntax
        self.num_invalid_syntax = num_invalid_syntax
        self.unrecognized_gene_symbols = unrecognized_gene_symbols
        self.num_unrecognized_gene_symbols = num_unrecognized_gene_symbols
        self.unrecognized_protein_residues = unrecognized_protein_residues
        self.num_unrecognized_protein_residues = num_unrecognized_protein_residues
        self.duplicates = duplicates
        self.num_duplicates = num_duplicates
        self.outside_of_structural_domain = outside_of_structural_domain
        self.num_outside_of_structural_domain = num_outside_of_structural_domain
        # additional information
        self.ELASPIC_URL = None
        self.uploaded_status = None
        self.downloaded_status = None
        # number of entries uploaded to ELASPIC in input recognition step.
        self.total_num_uploaded_entry = self.num_correctly_input_mutations + self.num_invalid_syntax \
                                        + self.num_unrecognized_gene_symbols \
                                        + self.num_unrecognized_protein_residues + self.num_duplicates \
                                        + self.num_outside_of_structural_domain

        # number of lines in text file.
        self.num_lines = self.get_num_lines()
        # after web page computation
        self.mutations_not_computed = None
        self.num_mutations_not_computed = None

    def set_muts_not_computed(self, mut_not_computed):
        logging.info("setting chunk's attr: `mut_not_computed`")
        self.mutations_not_computed = mut_not_computed['elements']
        self.num_mutations_not_computed = mut_not_computed['num_elements']

    def set_url(self, url):
        logging.info("setting chunk's attr: `ELASPIC_URL`")
        self.ELASPIC_URL = url

    def set_uploaded_status(self, uploaded_status):
        logging.info("setting chunk's attr: `uploaded_status`")
        self.uploaded_status = int(uploaded_status)

    def set_downloaded_status(self, downloaded_status):
        logging.info("setting chunk's attr: `downloaded_status`")
        self.downloaded_status = int(downloaded_status)

    def get_num_lines(self):
        """Returns number of lines in text file."""
        with open(self.file_path) as chunk_file:
            lines = chunk_file.readlines()
            lines = [line.strip() for line in lines if line.strip() != '']
            return len(lines)

    def parse_filename(self):
        """
        Parses the filepath

        Parameters
        ----------
            filepath : <todo>
                Filepath of chunkfile. E.g. SNV_BRCA_Chunk_22_0_test.txt
        Returns
        -------
            tcga_code, chunk_no, subchunk_no
        """
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

    def print_info(self):
        print("\t - - - CHUNK INFO - - - ")
        attributes = [attr for attr in dir(self) if not attr.startswith('__')]
        for attr in attributes:
            print(f"\t → {attr}: {getattr(self, attr)}")
