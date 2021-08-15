# import glob
# import logging
# from log_script import ColorHandler
# from driver_conf import initialize_driver
# from config import ELASPIC_MANY_URL
# from upload_utils import upload_file
# import os
# from pathlib import Path
#
# print("os.getcwd()", os.getcwd())
# # filepath = os.path.join(os.getcwd(), Path('input_files_test/SNV_BRCA_Chunk_X_X.txt'))
# # filepath = 'input_files_test/SNV_BRCA_Chunk_X_X.txt'
# # filepath = 'C:\\Users\\ibrah\\Documents\\GitHub\\My-ELASPIC-Web-API\\input_files_test\\SNV_BRCA_Chunk_X_X.txt'
# filepath = 'C:\\Users\\ibrah\\Documents\\GitHub\\My-ELASPIC-Web-API\\input_files_test\\SNV_BRCA_Chunk_X_X.txt'
# print("filepath::", filepath)
#
# log = logging.Logger('uploading file', level=logging.DEBUG)
# log.addHandler(ColorHandler())
#
# log.info("Starting uploading file debugger.")
#
# driver = initialize_driver()
# driver.get(ELASPIC_MANY_URL)
#
# upload_file(driver, filepath)
