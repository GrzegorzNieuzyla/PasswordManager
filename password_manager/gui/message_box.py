from PyQt5.QtWidgets import QMessageBox


def show_error(error: str) -> None:
    """
    Show error message box to a user
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText(error)
    msg.setWindowTitle("Error")
    msg.exec()


def confirm(msg: str) -> bool:
    """
    Show confirmation dialog and return whether a user has chosen 'YES'
    """
    result = QMessageBox.question(None, "Confirm action", msg,  # type: ignore
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    return result == QMessageBox.StandardButton.Yes
