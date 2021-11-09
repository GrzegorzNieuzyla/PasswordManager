from PyQt6.QtWidgets import QMessageBox


def show_error(error: str) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText(error)
    msg.setWindowTitle("Error")
    msg.exec()


def confirm(msg: str) -> bool:
    result = QMessageBox.question(None, "Confirm action", msg,
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  # type: ignore
    return result == QMessageBox.StandardButton.Yes
