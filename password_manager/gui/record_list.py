from typing import Dict, Callable, Optional

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from password_manager.models.record_data import RecordData


class RecordList(QListWidget):
    """
    GUI class for displaying and filtering record list
    """
    add_record_signal = pyqtSignal(RecordData)

    def __init__(self) -> None:
        super(RecordList, self).__init__()
        self.records: Dict[int, RecordData] = {}
        self.visible_items: Dict[int, QListWidgetItem] = {}
        self.clicked_handler: Optional[Callable[[RecordData], None]] = None
        self.double_clicked_handler: Optional[Callable[[RecordData], None]] = None
        self.itemClicked.connect(self._on_click)  # type: ignore
        self.itemDoubleClicked.connect(self._on_double_click)  # type: ignore
        self.add_record_signal.connect(self._add_to_record_list)  # type: ignore

    def add_record(self, record: RecordData) -> None:
        """
        Add given record to the view
        """
        if record.id_ in self.records:
            self.remove_record(record)
        self.records[record.id_] = record
        item = QListWidgetItem(record.title)
        item.setData(Qt.UserRole, record)
        self.addItem(item)
        self.visible_items[record.id_] = item
        self.sortItems(Qt.AscendingOrder)
        self.setCurrentItem(item)

    def remove_record(self, record: RecordData) -> None:
        """
        Removes record from the view
        """
        del self.records[record.id_]
        if record.id_ in self.visible_items:
            item = self.visible_items[record.id_]
            self.takeItem(self.row(item))
            del self.visible_items[record.id_]
        self.clearSelection()

    def set_on_clicked(self, callback: Callable[[RecordData], None]) -> None:
        self.clicked_handler = callback

    def set_on_double_clicked(self, callback: Callable[[RecordData], None]) -> None:
        self.double_clicked_handler = callback

    def _on_click(self, item: QListWidgetItem) -> None:
        if self.clicked_handler:
            self.clicked_handler(item.data(Qt.UserRole))

    def _on_double_click(self, item: QListWidgetItem) -> None:
        if self.double_clicked_handler:
            self.double_clicked_handler(item.data(Qt.UserRole))

    def clear_data(self) -> None:
        """
        Remove all records from view
        """
        self.clear()
        self.visible_items = {}
        self.records = {}

    def filter(self, query: str) -> None:
        """
        Hide records based on search query
        """
        self.visible_items = {}
        self.clear()
        for record in self.records.values():
            if query.lower() in record.title.lower():
                item = QListWidgetItem(record.title)
                item.setData(Qt.UserRole, record)
                self.addItem(item)
                self.visible_items[record.id_] = item
        self.sortItems(Qt.AscendingOrder)

    def clear_filter(self) -> None:
        self.filter("")

    @pyqtSlot(RecordData)
    def _add_to_record_list(self, record: RecordData) -> None:
        self.add_record(record)
