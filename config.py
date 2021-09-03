import pathlib

test_mode = False

ALLOWED_RAM_PERCENTAGE: int = 91

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
# ELASPIC_MANY_URL = 'about:neterror?e=netReset&u=http%3A//elaspic.kimlab.org/many/&c=UTF-8&d=The%20connection%20to%20the%20server%20was%20reset%20while%20the%20page%20was%20loading.'

HEADLESS = True
# coad=6 ov=12
ELASPIC_NUM_PARALLEL_COMPUTATION = 5

# r"C:\Users\ibrah\Desktop\Spaceship\ELASPIC_cancer_data_smaller_chunks\ELASPIC_Input\BRCA_10\SNV_BRCA_Chunk_22_0_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutations_input_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutation_input_test_40.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutations_input_test_10.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\mutation_all_error_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_0_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_1_test.txt"
# UPLOAD_FILE_PATH = r"C:\Users\ibrah\Documents\GitHub\My-ELASPIC-Web-API\input_files_test\SNV_BRCA_Chunk_22_7_test.txt"

# NOTIFY_AUDIO_PATH = "utils/alert_sounds/tr.mp3"
NOTIFY_NETWORK_ERROR_TRY_AUDIO_PATH = "utils/alert_sounds/network-error-trying-again.mp3"
NOTIFY_PROGRAM_NOT_WORKING_AUDIO_PATH = "utils/alert_sounds/program-not-working.mp3"

ALLOWED_ATTEMPTS = 5
