from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QWidget, QGridLayout, QLabel, QPushButton, QTextBrowser, QFrame

from client.BackendPackages.ClientKeywords import *


class ProfileInfoBox(QGroupBox):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(60, 40, 421, 290))
        self.name_label = QLabel(self)
        self.settings_button = QPushButton(self)
        self.bio_field = QTextBrowser(self)
        self.followers_label = QLabel(self)
        self.followings_label = QLabel(self)
        self.tweets_label = QLabel(self)
        self.setIntoGrid()

    def setIntoGrid(self):
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.settings_button, 0, 2, 1, 1)
        self.grid.addWidget(self.bio_field, 1, 0, 1, 3)
        self.grid.addWidget(self.followers_label, 2, 0, 1, 1)
        self.grid.addWidget(self.followings_label, 2, 1, 1, 1)
        self.grid.addWidget(self.name_label, 0, 0, 1, 1)
        self.grid.addWidget(self.tweets_label, 2, 2, 1, 1)

    def initiateTexts(self, user_info: dict[str, str]):
        self.setTitle(user_info[USERNAME])
        self.name_label.setText(user_info[NAME])
        self.settings_button.setText("Settings")
        self.followers_label.setText("Followers")
        self.followings_label.setText("Followings")
        self.tweets_label.setText("Tweets")


class ProfileHeaderBox(QFrame):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.grid = QGridLayout(self)
        self.profile_info_box = ProfileInfoBox(self)
        self.grid.addWidget(self.profile_info_box, 0, 0, 0, 0)

    def initiateTexts(self, user_info: dict[str, str]):
        self.profile_info_box.initiateTexts(user_info)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    a = ProfileHeaderBox()
    a.show()

    sys.exit(app.exec_())
