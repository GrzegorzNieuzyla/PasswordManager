import logging


class Logger:
    logger = logging.getLogger("Password manager")

    @staticmethod
    def set_level(level: int):
        logging.basicConfig()
        Logger.logger.setLevel(level)

    @staticmethod
    def info(msg: str):
        Logger.logger.info(msg)

    @staticmethod
    def error(msg: str):
        Logger.logger.error(msg)
