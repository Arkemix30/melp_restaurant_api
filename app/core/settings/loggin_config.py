import logging
import os

from dotenv import load_dotenv

LOG_FORMAT = "%(asctime)s %(name)-6s %(levelname)-4s %(message)s"
LOG_FILE_INFO = "logs.log"
LOG_FILE_ERROR = "error_log.log"

load_dotenv(override=True)

DEV = os.getenv("ENVIRONMENT") == "dev"


def get_logger(log_name=""):
    # Creating logger
    log = logging.getLogger(log_name)
    log_formatter = logging.Formatter(LOG_FORMAT)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)

    # File Handler
    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode="a")
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.DEBUG)

    if DEV:
        log.addHandler(file_handler_info)

    # Error handlers
    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode="a")
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)

    # Adding error handlers
    if DEV:
        log.addHandler(file_handler_error)
        log.addHandler(console_handler)

    log.setLevel(logging.DEBUG)

    return log
