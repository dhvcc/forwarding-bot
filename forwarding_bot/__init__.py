import logging

DEFAULT_FORMATTER = logging.Formatter("%(levelname)-7s [%(asctime)s] [%(name)s.%(funcName)s] = %(message)s",
                                      datefmt="%d.%m.%Y %H:%M")

DEBUG_FORMATTER = logging.Formatter("%(levelname)-7s [%(asctime)s] [%(name)s.%(funcName)s:%(lineno)s] = %(message)s",
                                    datefmt="%d.%m.%Y %H:%M")

logger = logging.getLogger("forwarding-bot")

if not logger.handlers:
    # Overall logging config
    logging.root.setLevel("INFO")

    # Logger initializing
    logger.setLevel("DEBUG")

    stream = logging.StreamHandler()
    stream.setFormatter(DEFAULT_FORMATTER)
    # stream.setLevel("INFO")
    stream.setLevel("DEBUG")
    logger.addHandler(stream)

    # TODO: add file handler

    logger.info("=====Bot logger initialized=====")
