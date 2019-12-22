import logging


def get_server_logger():

    logger = logging.getLogger("SERVER_LOGGER")

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        f_handler = logging.FileHandler('server.log')
        f_handler.setLevel(logging.DEBUG)

        f_format = logging.Formatter(fmt='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        f_handler.setFormatter(f_format)

        logger.addHandler(f_handler)
    return logger