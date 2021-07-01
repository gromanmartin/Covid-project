import logging

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('covidproject-log.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

c_format = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)