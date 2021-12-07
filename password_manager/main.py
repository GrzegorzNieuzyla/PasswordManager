import logging
import os.path
import sys

from PyQt5.QtWidgets import QApplication

from password_manager.application_context import ApplicationContext
from password_manager.utils.logger import Logger
from password_manager.utils.options import get_last_file


def run() -> None:
    """
    Initialize QApplication and run GUI
    """
    Logger.set_level(logging.ERROR)
    app = QApplication(sys.argv)
    application_context = ApplicationContext()
    application_context.initialize_integration_server('key.pem', 'cert.pem', 22222)
    last_db_file = get_last_file()
    if last_db_file and os.path.exists(last_db_file) and last_db_file.endswith(".pmdb"):
        application_context.initialize_database(last_db_file)
        application_context.login_controller.run_dialog()
    else:
        application_context.create_database_controller.run_dialog()
    app.exec()


if __name__ == "__main__":
    run()
