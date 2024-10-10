import logging
import os
from configs.config import LOGS_DIRECTORY

def get_logger(name):
    """
    Get a logger with the specified name.
    """
    os.makedirs(LOGS_DIRECTORY, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(os.path.join(LOGS_DIRECTORY, 'app.log'))
    console_handler = logging.StreamHandler()

    # Create formatters and add them to handlers
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger if they haven't been added already
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
