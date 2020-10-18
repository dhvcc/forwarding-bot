from ._bot import VKBot
import logging
from os.path import join

from forwarding_bot.settings import LOG_PATH, DEFAULT_FORMATTER

logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel("DEBUG")

    file = logging.FileHandler(join(LOG_PATH, "vk.log"))
    file.setFormatter(DEFAULT_FORMATTER)
    file.setLevel("DEBUG")
    logger.addHandler(file)

    logger.debug("=====Checker logger initialized=====")
