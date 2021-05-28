from PyQt5.QtWidgets import QMessageBox


def popBox(title: str, message: str, Qicon: int, std_buttons: list[int]):
    res = 0
    for num in std_buttons:
        res = res | num
    popup_window = QMessageBox(text=message)
    popup_window.setWindowTitle(title)
    popup_window.setIcon(Qicon)
    popup_window.setStandardButtons(res)
    popup_window.exec_()
