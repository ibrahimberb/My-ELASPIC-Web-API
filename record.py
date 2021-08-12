from chunk import Chunk
import pandas as pd
import os


class Record:
    def __init__(self, records_folder_path, tcga_type, chunk: Chunk):
        self.chunk = chunk
        self.records_folder_path = records_folder_path
        self.tcga_type = tcga_type
        self.filename = f"record_{tcga_type}_{chunk.chunk_code}_{chunk}"

    def create_record_file(self):
        record_file_path = os.path.join(self.records_folder_path, self.)
        if os.path.isfile(self.chunk.file_name):
            logging.info('File is downloaded.')

