import pathlib

COMPUTATION_TIME_ALLOWED = 1  # 3 # 10  # in seconds.
# Paths
DRIVER_PATH = r"C:\webdrivers\geckodriver.exe"
# r"C:\Users\ibrah\Desktop\Spaceship\ELASPIC_cancer_data_smaller_chunks\ELASPIC_Input\BRCA_10\SNV_BRCA_Chunk_22_0_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutations_input_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutation_input_test_40.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutations_input_test_10.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutation_all_error_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_0_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_1_test.txt"
UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_7_test.txt"
DOWNLOAD_FOLDER_PATH = pathlib.Path().resolve() / 'Firefox_download'
RECORDS_FOLDER_PATH = "Records_Test"
ELASPIC_MANY_URL = 'http://elaspic.kimlab.org/many/'
UPLOAD_FAILED_PATH = r"upload_failed_records.txt"
HEADLESS = True
