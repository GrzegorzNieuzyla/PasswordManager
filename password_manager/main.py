import logging
import sys

from PyQt6.QtWidgets import QApplication

from password_manager.application_context import ApplicationContext
from password_manager.utils.logger import Logger


def run() -> None:
    """
    Initialize QApplication and run GUI
    """
    Logger.set_level(logging.DEBUG)
    app = QApplication(sys.argv)
    application_context = ApplicationContext()
    application_context.initialize_integration_server('key.pem', 'cert.pem', 22222)
    application_context.create_database_controller.run_dialog()
    app.exec()


if __name__ == "__main__":
    run()
