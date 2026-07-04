import logging

def setup_logger(name: str = "trading_bot", log_file: str = "trading_bot.log", level=logging.INFO):
    """
    Sets up and returns a logger that writes detailed logs to a file only.
    Console output is handled separately via clean print statements.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler only - keeps full technical detail in trading_bot.log
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger