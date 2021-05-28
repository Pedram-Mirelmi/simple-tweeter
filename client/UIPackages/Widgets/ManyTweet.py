from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QScrollArea, QGridLayout, QApplication


class ManyTweetContainer(QWidget):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(0, 0, 629, 859))
        self.grid = QGridLayout(self)


class MultiTweetBox(QScrollArea):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.container = ManyTweetContainer()
        self.setWidget(self.container)
        self.setWidgetResizable(True)
        self.row_index = 1

    def setHeader(self, header: QWidget):
        self.header = header
        self.container.grid.addWidget(header, 0, 0, 1, 1)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    sys.exit(app.exec_())
