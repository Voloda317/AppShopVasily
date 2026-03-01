import logging
from logging.handlers import RotatingFileHandler

from src.config.config import settings

def setup_logging():
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(settings.LOG_LEVEL)

    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(settings.LOG_LEVEL)

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)