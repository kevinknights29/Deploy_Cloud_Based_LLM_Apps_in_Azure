import logging
import sys

import yaml
from yaml.loader import SafeLoader
from src.utils.constants import LOGGING_FORMAT
from src.utils.constants import CONFIG_FILE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(LOGGING_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

conf: dict = {}


def config() -> dict:
    """
    Loads the config.yaml file and returns a dict
    stored in config
    Returns:
        dict: configuration dictionary
    """

    global conf
    if not conf:
        with open(CONFIG_FILE, encoding="utf-8") as cfg:
            conf = yaml.load(cfg, Loader=SafeLoader)
        logger.log(logging.INFO, "Config loaded")
    return conf


def create_logger(logger_name, level=logging.INFO, fmt=LOGGING_FORMAT):
    """
    Creates and configures a logger object.

    Args:
        logger_name (str): The name of the logger.
        level (int): The log level to use (default: logging.INFO).

    Returns:
        logging.Logger: The configured logger object.
    """
    if logger_name in create_logger.loggers:
        return create_logger.loggers[logger_name]

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    formatter = logging.Formatter(fmt)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    create_logger.loggers[logger_name] = logger
    return logger


create_logger.loggers = {}
