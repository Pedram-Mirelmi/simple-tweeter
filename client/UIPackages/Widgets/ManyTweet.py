from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QScrollArea, QGridLayout, QApplication
from .WriteTweet import WriteTweetBox
from .ProfileHeader import *

class ManyTweetContainer(QWidget):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(0, 0, 629, 859))
        self.grid = QGridLayout(self)


class ManyTweetBox(QScrollArea):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.t_container = ManyTweetContainer()
        self.setWidget(self.t_container)
        self.setWidgetResizable(True)
        self.row_index = 1

    def addWriteTweetHeader(self, username: str):
        self.header = WriteTweetBox(self.t_container)
        self.header.initiateBox(username)
        self.t_container.grid.addWidget(self.header, 0, 0, 1, 1)

    def addProfileInfoHeader(self, profile_info: dict[str, str]):  # TODO
        self.header = ProfileInfoBox(self.t_container)
        self.header.initiateTexts(profile_info)
        self.t_container.grid.addWidget(self.header, 0, 0, 1, 1)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    sys.exit(app.exec_())
