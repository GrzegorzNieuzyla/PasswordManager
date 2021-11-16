from typing import Callable

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu, QApplication


class MenuBar(QMenuBar):
    def __init__(self) -> None:
        super(MenuBar, self).__init__()
        self.file_menu: QMenu = self.addMenu("&File")
        self.options_menu: QMenu = self.addMenu("&Options")
        self.new_db_action: QAction = self.file_menu.addAction("&Add new database file")
        self.open_db_action: QAction = self.file_menu.addAction("Open &database file")
        self.quit_action: QAction = self.file_menu.addAction("&Quit")
        self.quit_action.triggered.connect(lambda: QApplication.quit())  # type: ignore
        self.preferences_action = self.options_menu.addAction("&Preferences")
        self.file_menu.setMinimumWidth(250)
        self.options_menu.setMinimumWidth(150)

    def set_on_new_db(self, callback: Callable[[], None]) -> None:
        self.new_db_action.triggered.connect(callback)  # type: ignore

    def set_on_open_db(self, callback: Callable[[], None]) -> None:
        self.open_db_action.triggered.connect(callback)  # type: ignore

    def set_on_preferences(self, callback: Callable[[], None]) -> None:
        self.preferences_action.triggered.connect(callback)  # type: ignore
