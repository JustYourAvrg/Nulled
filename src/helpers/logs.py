import logging


logging.basicConfig(
    filename='logs.log',
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode='a'
)


def handle_log_msg(type: str, msg: str):
    if type == 'ERROR':
        logging.error(msg)
    elif type == 'DEBUG':
        logging.debug(msg)
    elif type == 'INFO':
        logging.info(msg)