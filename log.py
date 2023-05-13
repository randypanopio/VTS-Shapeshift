import logging

formatter = logging.Formatter('%(asctime)s %(funcName)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')

# Configure basic logging settings
logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s %(funcName)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

# Create a file handler
file_handler = logging.FileHandler('test.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create a logger
ws_logger = logging.getLogger('ws_logger')
ws_logger.setLevel(logging.DEBUG)
ws_logger.addHandler(file_handler)
