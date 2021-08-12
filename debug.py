import logging

logging.basicConfig(filename='mylog.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

logging.debug("this is debug")
logging.info("this is info")
logging.warning("this is warning")
logging.error("this is error")
logging.critical("this is critical")
# this needs to be RED.
print("10 / 0 =", 10 / 0)
