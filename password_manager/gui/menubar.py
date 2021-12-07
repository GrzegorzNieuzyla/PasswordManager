from typing import Callable

from PyQt5.QtWidgets import QMenuBar, QMenu, QApplication, QAction


class MenuBar(QMenuBar):
    """
    Menu bar listing File options
    """

    def __init__(self) -> None:
        super(MenuBar, self).__init__()
        self.file_menu: QMenu = self.addMenu("&File")
        self.new_db_action: QAction = self.file_menu.addAction("&Add new database file")
        self.open_db_action: QAction = self.file_menu.addAction("Open &database file")
        self.options_actions: QAction = self.file_menu.addAction("&Options")
        self.quit_action: QAction = self.file_menu.addAction("&Quit")
        self.quit_action.triggered.connect(lambda: QApplication.quit())  # type: ignore
        self.file_menu.setMinimumWidth(250)

    def set_on_new_db(self, callback: Callable[[], None]) -> None:
        self.new_db_action.triggered.connect(callback)  # type: ignore

    def set_on_open_db(self, callback: Callable[[], None]) -> None:
        self.open_db_action.triggered.connect(callback)  # type: ignore

    def set_on_options(self, callback: Callable[[], None]) -> None:
        self.options_actions.triggered.connect(callback)  # type: ignore
