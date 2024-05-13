import logging

stream_handler = logging.StreamHandler()
logger = logging.getLogger("API_LOGER")
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
