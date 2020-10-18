import logging
import os
from datetime import datetime

import pytz

PARSE_MODE = "HTML"

# Timezone
MINSK_TZ = pytz.timezone("Europe/Minsk")


def minsk_timezone(*args):
    return datetime.now(MINSK_TZ).timetuple()


# Logging
LOG_PATH = os.path.join("log")
DEFAULT_FORMATTER = logging.Formatter("%(levelname)-7s [%(asctime)s] [%(name)s.%(funcName)s] = %(message)s",
                                      datefmt="%d.%m.%Y %H:%M")

DEBUG_FORMATTER = logging.Formatter("%(levelname)-7s [%(asctime)s] [%(name)s.%(funcName)s:%(lineno)s] = %(message)s",
                                    datefmt="%d.%m.%Y %H:%M")
