import os
import sys
import logging


logger = logging.getLogger('aiossdb')

logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stderr)
handler.setFormatter(logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"))
logger.addHandler(handler)
os.environ["AIOSSDB_DEBUG"] = ""
