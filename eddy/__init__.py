import logging
import logging.handlers

def _getLogger():
    global logger
    logger = logging.getLogger('EddyLogger')
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

_getLogger()