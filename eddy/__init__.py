import logging
import logging.handlers

def _getLogger():
    global logger
    _logger = logging.getLogger('EddyLogger')
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)
    _logger.setLevel(logging.INFO)
    logger = _logger


_getLogger()