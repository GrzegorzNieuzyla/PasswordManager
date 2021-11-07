from PyQt6.QtWidgets import QMessageBox


def show_error(error: str):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText(error)
    msg.setWindowTitle("Error")
    msg.exec()
