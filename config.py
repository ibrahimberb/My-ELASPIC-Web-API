import pathlib

test_mode = False

if test_mode:
    RECORDS_FOLDER_PATH = r"test_files\Records_Test"
    ELASPIC_RESULTS_FOLDER_PATH = r"test_files\ELASPIC_Results_TEST"
    UPLOAD_FAILED_PATH = r"test_files\upload_failed_records_TEST"
    UNEXPECTED_FAILED_PATH = r"test_files\unexpected_failed_records_TEST"
    INPUT_FILES_PATH = r"test_files\input_files_test"
    ALLMUTATIONS_FAILED_PATH = r"test_files\allmutations_failed_TEST"

# ACTUAL RUN
else:
    RECORDS_FOLDER_PATH = "Records"
    ELASPIC_RESULTS_FOLDER_PATH = "Elaspic_Results"
    UPLOAD_FAILED_PATH = "Upload_fails"
    UNEXPECTED_FAILED_PATH = "Unexpected_fails"
    INPUT_FILES_PATH = "ELASPIC_Input"
    ALLMUTATIONS_FAILED_PATH = r"Allmutations_fails"

COMPUTATION_TIME_ALLOWED = 1  # 3 # 10  # in seconds.

# Paths
DRIVER_PATH = r"C:\webdrivers\geckodriver.exe"
TEMP_DOWNLOAD_FOLDER_PATH = pathlib.Path().resolve() / 'Firefox_download'
ELASPIC_MANY_URL = 'http://elaspic.kimlab.org/many/'

HEADLESS = True
ELASPIC_NUM_PARALLEL_COMPUTATION = 10

# r"C:\Users\ibrah\Desktop\Spaceship\ELASPIC_cancer_data_smaller_chunks\ELASPIC_Input\BRCA_10\SNV_BRCA_Chunk_22_0_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutations_input_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutation_input_test_40.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutations_input_test_10.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutation_all_error_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_0_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_1_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_7_test.txt"
