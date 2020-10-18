import pkg_resources
import logging

logger = logging.getLogger(__name__)

SUPPORTED_MODULES = ["ujson", ]  # In speed increase order
DOWNLOADED = [
    pkg.key for pkg in pkg_resources.working_set if pkg.key in SUPPORTED_MODULES
]
MODULE = DOWNLOADED[-1] if DOWNLOADED else "json"

logger.info(f"Using {MODULE} as JSON parsing library")

json = __import__(MODULE)
