from chunk import Chunk
import pandas as pd
import os
import logging
from utils import get_filename_from_path

logging.basicConfig(filename='recordlogger.log', level=logging.INFO, format='%(message)s')


class RecordStatuses:
    NOT_RECORDED = "NOT_RECORDED"
    RECORDED_NOT_DOWNLOADED = "RECORDED_NOT_DOWNLOADED"
    RECORDED_DOWNLOADED = "RECORDED_DOWNLOADED"


# def is_subchunk_completed(self):
#     completed_condition = (self.chunk.ELASPIC_URL is not None and
#                            self.chunk.uploaded_status is True and
#                            self.chunk.downloaded_status is True)
#
#     return completed_condition


def get_chunk_record_status(chunk_file_path, records_folder_path):
    record = Record(records_folder_path, Chunk(chunk_file_path))

    # print("dir(record)", dir(record))
    # print("RECORD_DATA")
    # print('-----------------------------------')
    # print(record.record_data['ELASPIC_URL'])
    # print('-----------------------------------')

    logging.info(f"record_data shape: {record.record_data.shape}")

    # print('-----------------------------------')
    # print("record.chunk.file_name:", record.chunk.file_name)
    # print('-----------------------------------')
    # print("record.record_data.index:", record.record_data.index)
    # print('-----------------------------------')

    if record.chunk.file_name not in record.record_data.index:
        return RecordStatuses.NOT_RECORDED, None
    # print('-----------------------------------')
    # print('apperantly, I can find the index and access it..')
    # print(record.chunk.file_name in record.record_data.index)
    # print('-----------------------------------')

    # print("record.chunk.file_name:", record.chunk.file_name)

    # print('-----------------------------------')
    entry_data = record.record_data.loc[[record.chunk.file_name]]
    # print("ENTRY DATA")
    # print('entry_data', entry_data)
    # print('entry_data.shape', entry_data.shape)
    # print('entry_data ELASPIC URL', entry_data.loc[record.chunk.file_name, 'ELASPIC_URL'])
    # print('-----------------------------------')

    # print('-----------------------------------')
    # print('record.chunk.file_path:', record.chunk.file_path)
    # print('-----------------------------------')
    # chunk_filename = get_filename_from_path(record.chunk.file_path)
    # print('chunk_filename:', chunk_filename)
    # print('-----------------------------------')

    instanciate_dict = {}
    for colname in list(entry_data.columns):
        instanciate_dict[colname.lower()] = entry_data.loc[record.chunk.file_name, colname]
        # print(f'adding value {colname.lower()} = {entry_data.loc[record.chunk.file_name, colname]} to dictionary .. ')

    # print("instanciate_dict")
    # print(instanciate_dict)
    # print('-----------------------------------')
    # print("record.chunk.file_path:::::", record.chunk.file_path)
    # print('-----------------------------------')

    # print('READ ELASPIC URL: ', entry_data.loc[chunk_filename, 'ELASPIC_URL'])

    # todo maybe kwargs and args might be useful here.............!!!!.
    chunk = Chunk(file_path=record.chunk.file_path,
                  num_correctly_input_mutations=instanciate_dict['num_correctly_input_mutations'],
                  invalid_syntax=instanciate_dict['invalid_syntax'],
                  num_invalid_syntax=instanciate_dict['num_invalid_syntax'],
                  unrecognized_gene_symbols=instanciate_dict['unrecognized_gene_symbols'],
                  num_unrecognized_gene_symbols=instanciate_dict['num_unrecognized_gene_symbols'],
                  unrecognized_protein_residues=instanciate_dict['unrecognized_protein_residues'],
                  num_unrecognized_protein_residues=instanciate_dict['num_unrecognized_protein_residues'],
                  duplicates=instanciate_dict['duplicates'], num_duplicates=instanciate_dict['num_duplicates'],
                  outside_of_structural_domain=instanciate_dict['outside_of_structural_domain'],
                  num_outside_of_structural_domain=instanciate_dict['num_outside_of_structural_domain'],
                  elaspic_url=instanciate_dict['elaspic_url'],
                  uploaded_status=instanciate_dict['uploaded_status'],
                  downloaded_status=instanciate_dict['downloaded_status'])

    # todo clean this mess
    # print('-----------------------------------')
    # print('------- controlling chunk ---------')
    # print('-----------------------------------')
    # print("CHUNK INFO")
    # chunk.print_info()

    if (
            entry_data.loc[record.chunk.file_name, 'UPLOADED_STATUS'] == 1 and
            entry_data.loc[record.chunk.file_name, 'DOWNLOADED_STATUS'] == 1
    ):
        # print('returning chunk with URL: ', chunk.elaspic_url)
        return RecordStatuses.RECORDED_DOWNLOADED, chunk  # chunk.ELASPIC_URL, chunk

    elif (
            entry_data.loc[record.chunk.file_name, 'UPLOADED_STATUS'] == 1 and
            entry_data.loc[record.chunk.file_name, 'DOWNLOADED_STATUS'] == 0
    ):
        # print('returning chunk with URL: ', chunk.elaspic_url)
        return RecordStatuses.RECORDED_NOT_DOWNLOADED, chunk  # entry_data.loc[record.chunk.file_name, 'ELASPIC_URL'], chunk

    else:
        raise Exception('something went wrong :(')


class Record:
    # COLUMN_NAMES_TO_CHUNK_ATTR = \
    #     {
    #         'SUBCHUNK': "file_name",
    #         'NUM_CORR_INPUT_MUTS': "num_correctly_input_mutations",
    #         'INVALID_SYNTAX': "invalid_syntax",
    #         'NUM_INVALID_SYNTAX': "num_invalid_syntax",
    #         'UNRECOG_GENE_SYMBOLS': "unrecognized_gene_symbols",
    #         'NUM_UNRECOG_GENE_SYMBOLS': "num_unrecognized_gene_symbols",
    #         'UNRECOG_PROT_RESIDUES': "unrecognized_protein_residues",
    #         'NUM_UNRECOG_PROT_RESIDUES': "num_unrecognized_protein_residues",
    #         'DUPLICATES': "duplicates",
    #         'NUM_DUPLICATES': "num_duplicates",
    #         'OUTSIDE_STRUCT_DOMAIN': "outside_of_structural_domain",
    #         'NUM_OUTSIDE_STRUCT_DOMAIN': "num_outside_of_structural_domain",
    #         'NUM_ACTUAL_INPUT': "num_lines",
    #         'NUM_PROVIDED_INPUT': "total_num_uploaded_entry",
    #         'ELASPIC_URL': "ELASPIC_URL",
    #         'UPLOADED_STATUS': 'uploaded_status',
    #         'DOWNLOADED_STATUS': 'downloaded_status'
    #     }

    # COLUMN_NAMES = list(COLUMN_NAMES_TO_CHUNK_ATTR.keys())

    def __init__(self, records_folder_path, chunk: Chunk):
        self.chunk = chunk
        self.records_folder_path = records_folder_path
        self.tcga_code = chunk.tcga_code
        self.filename = f"record_{chunk.tcga_code}_{chunk.chunk_no}.csv"
        self.path = os.path.join(self.records_folder_path, self.filename)
        self.COLUMN_NAMES_TO_CHUNK_ATTR = None
        self.COLUMN_NAMES = None
        self.prepare_colnames()
        self.record_data = self.bring_record()
        self.initialize_record_file()

    def update(self):
        record_data = self.bring_record()
        record_data.loc[[self.chunk.file_name]] = self.get_new_chunk_entry().loc[[self.chunk.file_name]]
        return record_data

    def get_new_chunk_entry(self):
        new_chunk_entry = self.create_record()

        for column in new_chunk_entry.columns:
            new_chunk_entry.loc[self.chunk.file_name, column] = getattr(self.chunk,
                                                                        self.COLUMN_NAMES_TO_CHUNK_ATTR[column])

        return new_chunk_entry

    def record(self):
        record_data = self.bring_record()
        # if subchunk name is not found in the table, record it to the table.
        if self.chunk.file_name not in record_data.index:
            logging.debug(f'Appending {self.chunk.file_name}')
            record_data = record_data.append(self.get_new_chunk_entry())

        else:
            record_data = self.update()

        record_data.to_csv(self.path)

    def initialize_record_file(self):
        if not os.path.isfile(self.path):
            logging.info('creating record file {} ...'.format(self.filename))
            self.write_record()

        else:
            logging.info(f"record file {self.filename} already exist, no need to create a new one.")

    def bring_record(self):
        if self.is_exist():
            logging.debug('bringing from existing file.')
            record_data = self.read_record()
        else:
            record_data = self.create_record()
        # print('debug - bring_record: record_data.index.name: ', record_data.index.name)
        return record_data

    def create_record(self):
        record_data = pd.DataFrame(columns=self.COLUMN_NAMES).set_index(self.COLUMN_NAMES[0])
        logging.debug('Creating record ..')
        # print('debug - create_record: record_data.index.name: ', record_data.index.name)
        return record_data

    def read_record(self):
        record_data = pd.read_csv(self.path, index_col=self.COLUMN_NAMES[0])
        # print('debug - read_record: record_data.index.name: ', record_data.index.name)
        return record_data

    def write_record(self):
        logging.debug('Writing record ..')
        self.record_data.to_csv(self.path)

    def is_exist(self):
        logging.debug(f'checking if {self.path} exist.')
        return os.path.isfile(self.path)

    def prepare_colnames(self):
        self.COLUMN_NAMES_TO_CHUNK_ATTR = {attr.upper(): attr for attr in self.chunk.get_attributes()}
        self.COLUMN_NAMES = list(self.COLUMN_NAMES_TO_CHUNK_ATTR.keys())
