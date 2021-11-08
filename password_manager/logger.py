import logging


class Logger:
    logger = logging.getLogger("Password manager")

    @staticmethod
    def set_level(level: int) -> None:
        logging.basicConfig()
        Logger.logger.setLevel(level)

    @staticmethod
    def info(msg: str) -> None:
        Logger.logger.info(msg)

    @staticmethod
    def error(msg: str) -> None:
        Logger.logger.error(msg)
