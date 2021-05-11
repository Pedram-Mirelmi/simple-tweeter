from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QScrollArea, QGridLayout, QApplication


class ManyTweetContainer(QWidget):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(0, 0, 629, 859))
        self.grid = QGridLayout(self)


class ManyTweetBox(QScrollArea):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.resize(652, 880)
        self.setGeometry(QtCore.QRect(11, 10, 631, 861))
        self.setWidgetResizable(True)
        self.setObjectName("scrollArea")
        self.t_container = ManyTweetContainer()
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.t_container)
        self.setWidget(self.t_container)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    sys.exit(app.exec_())
