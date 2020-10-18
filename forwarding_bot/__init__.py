import logging
from os import mkdir
from os.path import join, isdir

from forwarding_bot.settings import DEFAULT_FORMATTER, DEBUG_FORMATTER, LOG_PATH, minsk_timezone

logger = logging.getLogger(__name__)
if not logger.handlers:
    # Dir check
    if not isdir(LOG_PATH):
        mkdir(LOG_PATH)
    # Overall logging config
    logging.root.setLevel("INFO")
    logging.Formatter.converter = minsk_timezone

    # Logger initializing
    logger.setLevel("DEBUG")

    stream = logging.StreamHandler()
    stream.setFormatter(DEFAULT_FORMATTER)
    stream.setLevel("INFO")
    # stream.setLevel("DEBUG")
    logger.addHandler(stream)

    file = logging.FileHandler(join(LOG_PATH, "forwarding_bot.log"))
    file.setFormatter(DEFAULT_FORMATTER)
    file.setLevel("DEBUG")
    logger.addHandler(file)

    logger.info("=====Bot logger initialized=====")
