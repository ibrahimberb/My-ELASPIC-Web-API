from record import Record
from chunk import Chunk

toy_path = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_0_test.txt"

mychunk = Chunk(file_path=toy_path)

mychunk.print_info()
print('======================================================')
myrecord = Record("records_path_testing", mychunk)
print(myrecord.COLUMN_NAMES)
myrecord.record(mychunk)
