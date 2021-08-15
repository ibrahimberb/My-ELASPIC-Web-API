import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)-25s : %(levelname)-10s : %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("saving the results")
logger.critical("CRITICAL")
