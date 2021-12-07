import os
from typing import Optional

from PyQt5.QtWidgets import QFileDialog

from password_manager.gui.message_box import show_error


class FileHelper:
    @staticmethod
    def open_db_file() -> Optional[str]:
        """
        Show dialog for opening files, validate and return path
        """
        filename: str
        filename, _ = QFileDialog.getOpenFileName(filter="Password manager database file (*.pmdb)",
                                                  caption="Choose database file")
        if not filename:
            return None
        if not filename.endswith(".pmdb"):
            show_error("Not a database file")
            return None
        if not os.path.exists(filename):
            show_error(f"File {filename} does not exist")
            return None
        return filename

    @staticmethod
    def open_db_file_for_writing() -> str:
        """
        Show dialog for new file
        """
        filename: str
        filename, _ = QFileDialog.getSaveFileName(filter="Password manager database file (*.pmdb)",
                                                  caption="Choose new database file")
        return filename
