import os, logging

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
    )

def get_log_level(file_variable: str) -> int:
    logging_variable = "LOG_LEVEL_" + file_variable
    log_level = int(os.getenv("LOG_LEVEL")) if os.getenv("LOG_LEVEL") else logging.INFO
    if os.getenv(logging_variable):
        log_level = int(os.getenv(logging_variable))
    
    return log_level

def get_logger(name: str) -> logging.Logger:
    log_level = get_log_level(file_variable=name)
    logger = logging.getLogger(name="file_variable")
    logging.debug(msg=f"Setting log level {logging.getLevelName(log_level)} for {name}")
    logger.setLevel(log_level)
    return logger
