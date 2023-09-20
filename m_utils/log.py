import logging

formatter = logging.Formatter('%(asctime)s %(funcName)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')

# Configure basic logging settings
logging.basicConfig(filename='output.log', level=logging.DEBUG, format='%(asctime)s %(funcName)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
file_handler = logging.FileHandler('output.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create a stream handler for printing to the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# Create the logger and add both file and stream handlers
ws_logger = logging.getLogger('ws_logger')
ws_logger.setLevel(logging.DEBUG)
ws_logger.addHandler(file_handler)
ws_logger.addHandler(stream_handler)