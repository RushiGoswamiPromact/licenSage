import logging

import colorlog


def create_console_handler():
    """
    Create a console handler for logging.

    Returns:
        logging.StreamHandler: A console handler for logging.

    This function creates a console handler for logging. It sets the log level to DEBUG and configures a colored formatter
    with custom log colors for different log levels. The formatter formats the log message with the log color, timestamp,
    logger name, log level, and message. The function then sets the formatter on the console handler and returns it.
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
    console_handler.setFormatter(formatter)
    return console_handler


def get_logger(name: str):
    """
    Returns a logger object with the specified name.

    Parameters:
        name (str): The name of the logger.

    Returns:
        logging.Logger: A logger object with the specified name.

    This function creates a logger object with the specified name and sets its log level to the value of the
    environment variable. It also adds a console handler and a Seq handler (if enabled) to the logger. If file logging is
    enabled, it adds a file handler to the logger. The function returns the logger object.
    """
    logger = logging.getLogger(name)

    # if not logger.handlers:
    logger.setLevel("INFO")
    console_handler = create_console_handler()

    logger.addHandler(console_handler)
    return logger


def log_startup_to_console():
    """
    Logs the startup information to the console.

    This function creates a logger object for the "startup" name and sets its log level to the value of the
    environment variable. It then logs the value of  using the info level. If seq_enabled() returns True,
    it logs "Seq log enabled". If file_enabled() returns True, it logs "File logging enabled".

    Returns:
        None
    """
    startup_logger = get_logger("startup")
    startup_logger.info("Starting up LOGS...")


log_startup_to_console()

logger = get_logger(__name__)
