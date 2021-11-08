import logging
import sys

from PyQt6.QtWidgets import QApplication

from password_manager.application_context import ApplicationContext
from password_manager.logger import Logger


def run() -> None:
    Logger.set_level(logging.DEBUG)
    app = QApplication(sys.argv)
    application_context = ApplicationContext()
    application_context.create_database_controller.run_dialog()
    app.exec()


if __name__ == "__main__":
    run()
