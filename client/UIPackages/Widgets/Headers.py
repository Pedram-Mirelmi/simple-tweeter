from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QWidget, QGridLayout, \
    QLabel, QPushButton, QTextBrowser, QTextEdit

from client.BackendPackages.ClientKeywords import *


class WriteItemHeader(QGroupBox):
    def __init__(self, mother_area: QWidget = None, item_type: str = None):
        super().__init__(mother_area)
        self.item_type = item_type
        self.setGeometry(QtCore.QRect(270, 40, 450, 244))
        self.setMinimumSize(QtCore.QSize(450, 244))
        self.setMaximumSize(QtCore.QSize(450, 250))
        self.gridLayout = QGridLayout(self)
        self.item_text_field = QTextEdit(self)
        self.gridLayout.addWidget(self.item_text_field, 0, 0, 1, 1)
        self.send_button = QPushButton(self)
        self.gridLayout.addWidget(self.send_button, 1, 0, 1, 1)

    def initiateTexts(self, username: str):
        self.setTitle(f"Write {self.item_type} as '{username}':")
        self.send_button.setText("Send")


class ProfileInfoHeader(QGroupBox):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(60, 40, 421, 290))
        self.name_label = QLabel(self)
        self.bio_field = QTextBrowser(self)
        self.followers_label = QLabel(self)
        self.followings_label = QLabel(self)
        self.tweets_label = QLabel(self)
        self.setIntoGrid()

    def setIntoGrid(self):
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.bio_field, 1, 0, 1, 3)
        self.grid.addWidget(self.followers_label, 2, 0, 1, 1)
        self.grid.addWidget(self.followings_label, 2, 1, 1, 1)
        self.grid.addWidget(self.name_label, 0, 0, 1, 1)
        self.grid.addWidget(self.tweets_label, 2, 2, 1, 1)

    def initiateTexts(self, user_info: dict[str, str]):
        self.setTitle(user_info[USERNAME])
        self.name_label.setText(user_info[NAME])
        self.followers_label.setText(f"Followers({user_info[FOLLOWERS]})")
        self.followings_label.setText(f"Followings({user_info[FOLLOWINGS]})")
        self.tweets_label.setText(f"Tweets({user_info[TWEETS]})")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    a = ProfileInfoHeader()
    a.show()

    sys.exit(app.exec_())
