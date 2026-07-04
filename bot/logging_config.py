import logging
import os

def setup_logger(name: str = "trading_bot", log_file: str = "trading_bot.log", level=logging.INFO):
    """
    Sets up and returns a logger that writes to both a file and the console.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers if this is called multiple times
    if logger.handlers:
        return logger

    # Format: timestamp - log level - message
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler - writes logs to trading_bot.log
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Console handler - also prints logs to terminal (helpful while testing)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger