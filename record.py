from chunk import Chunk
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def has_recorded(chunk_file_path, records_folder_path):
    record = Record(records_folder_path, Chunk(chunk_file_path))
    logging.info(f"record_data shape: {record.record_data.shape}")
    return record.chunk.file_name in record.record_data.index


class Record:
    COLUMN_NAMES_TO_CHUNK_ATTR = \
        {
            'SUBCHUNK': "file_name",
            'ELASPIC_URL': "ELASPIC_URL",
            'NUM_CORR_INPUT_MUTS': "num_correctly_input_mutations",
            'INVALID_SYNTAX': "invalid_syntax",
            'NUM_INVALID_SYNTAX': "num_invalid_syntax",
            'UNRECOG_GENE_SYMBOLS': "unrecognized_gene_symbols",
            'NUM_UNRECOG_GENE_SYMBOLS': "num_unrecognized_gene_symbols",
            'UNRECOG_PROT_RESIDUES': "unrecognized_protein_residues",
            'NUM_UNRECOG_PROT_RESIDUES': "num_unrecognized_protein_residues",
            'DUPLICATES': "duplicates",
            'NUM_DUPLICATES': "num_duplicates",
            'OUTSIDE_STRUCT_DOMAIN': "outside_of_structural_domain",
            'NUM_OUTSIDE_STRUCT_DOMAIN': "num_outside_of_structural_domain",
            'NUM_ACTUAL_INPUT': "num_lines",
            'NUM_PROVIDED_INPUT': "total_num_uploaded_entry"
        }

    COLUMN_NAMES = list(COLUMN_NAMES_TO_CHUNK_ATTR.keys())

    def __init__(self, records_folder_path, chunk: Chunk):
        self.chunk = chunk
        self.records_folder_path = records_folder_path
        self.tcga_code = chunk.tcga_code
        self.filename = f"record_{chunk.tcga_code}_{chunk.chunk_no}.csv"
        self.path = os.path.join(self.records_folder_path, self.filename)
        self.record_data = self.bring_record()
        self.initialize_record_file()

    def is_subchunk_completed(self):
        completed_condition = (self.chunk.ELASPIC_URL is not None and
                               self.chunk.uploaded_status is True and
                               self.chunk.downloaded_status is True)

        return completed_condition

    def update_record_data(self, updated_record_data):
        self.record_data = updated_record_data

    def get_new_chunk_entry(self):
        new_chunk_entry = self.create_record()
        print('new_chunk_entry columns:')
        for column in new_chunk_entry.columns:
            print(' - - - - - - - - - - ')
            new_chunk_entry.loc[self.chunk.file_name, column] = getattr(self.chunk,
                                                                        self.COLUMN_NAMES_TO_CHUNK_ATTR[column])

        print('new_chunk_entry')
        print(new_chunk_entry)
        return new_chunk_entry

    def record(self):
        record_data = self.bring_record()

        # if subchunk name is not found in the table, record it to the table.
        if self.chunk.file_name not in record_data.index:
            logging.info(f'Appending {self.chunk.file_name}')
            record_data = record_data.append(self.get_new_chunk_entry())

        print('APPENDED DATA')
        print(record_data)

        record_data.to_csv(self.path)
        # self.update_record_data(record_data)
        # self.write_record()

        # todo idk
        # self.
        # if record_data.loc[[chunk.subchunk_no]]

    def initialize_record_file(self):
        if not os.path.isfile(self.path):
            logging.info('creating record file {} ...'.format(self.filename))
            self.write_record()

        else:
            logging.info("record file {} already exist, we don't touch it..")

    def bring_record(self):
        if self.is_exist():
            record_data = self.read_record()
        else:
            record_data = self.create_record()
        return record_data

    def create_record(self):
        record_data = pd.DataFrame(columns=self.COLUMN_NAMES).set_index(self.COLUMN_NAMES[0])
        logging.info('Creating record ..')
        return record_data

    def read_record(self):
        record_data = pd.read_csv(self.path, index_col=self.COLUMN_NAMES[0])
        return record_data

    def write_record(self):
        logging.info('Writing record ..')
        self.record_data.to_csv(self.path)

    def is_exist(self):
        return os.path.isfile(self.path)
