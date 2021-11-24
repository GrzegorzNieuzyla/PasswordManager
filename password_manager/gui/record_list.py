from typing import Dict, Callable, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidget, QListWidgetItem

from password_manager.models.record_data import RecordData


class RecordList(QListWidget):
    def __init__(self) -> None:
        super(RecordList, self).__init__()
        self.records: Dict[int, RecordData] = {}
        self.visible_items: Dict[int, QListWidgetItem] = {}
        self.clicked_handler: Optional[Callable[[RecordData], None]] = None
        self.double_clicked_handler: Optional[Callable[[RecordData], None]] = None
        self.itemClicked.connect(self._on_click)  # type: ignore
        self.itemDoubleClicked.connect(self._on_double_click)  # type: ignore

    def add_record(self, record: RecordData) -> None:
        if record.id_ in self.records:
            self.remove_record(record)
        self.records[record.id_] = record
        item = QListWidgetItem(record.title)
        item.setData(Qt.ItemDataRole.UserRole, record)
        self.addItem(item)
        self.visible_items[record.id_] = item
        self.sortItems(Qt.SortOrder.AscendingOrder)
        self.setCurrentItem(item)

    def remove_record(self, record: RecordData) -> None:
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
            self.clicked_handler(item.data(Qt.ItemDataRole.UserRole))

    def _on_double_click(self, item: QListWidgetItem) -> None:
        if self.double_clicked_handler:
            self.double_clicked_handler(item.data(Qt.ItemDataRole.UserRole))

    def clear_data(self) -> None:
        self.clear()
        self.visible_items = {}
        self.records = {}

    def filter(self, query: str) -> None:
        self.visible_items = {}
        self.clear()
        for record in self.records.values():
            if query.lower() in record.title.lower():
                item = QListWidgetItem(record.title)
                item.setData(Qt.ItemDataRole.UserRole, record)
                self.addItem(item)
                self.visible_items[record.id_] = item
        self.sortItems(Qt.SortOrder.AscendingOrder)

    def clear_filter(self) -> None:
        self.filter("")
