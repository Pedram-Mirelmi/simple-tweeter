# not used yet

from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QWidget, QGridLayout, QLabel, QPushButton, QTextBrowser


class ProfileInfoBox(QGroupBox):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(60, 40, 421, 290))
        self.grid = QGridLayout(self)
        self.name_label = QLabel(self)
        self.grid.addWidget(self.name_label, 0, 0, 1, 1)
        self.settings_button = QPushButton(self)
        self.grid.addWidget(self.settings_button, 0, 2, 1, 1)
        self.bio_field = QTextBrowser(self)
        self.grid.addWidget(self.bio_field, 1, 0, 1, 3)
        self.followers_label = QLabel(self)
        self.grid.addWidget(self.followers_label, 2, 0, 1, 1)
        self.followings_label = QLabel(self)
        self.grid.addWidget(self.followings_label, 2, 1, 1, 1)
        self.tweets_label = QLabel(self)
        self.grid.addWidget(self.tweets_label, 2, 2, 1, 1)

        self.initiateTexts()

    def initiateTexts(self):
        self.setTitle("Username")
        self.name_label.setText("Name")
        self.settings_button.setText("Settings")
        self.followers_label.setText("Followers")
        self.followings_label.setText("Followings")
        self.tweets_label.setText("Tweets")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)


    a = ProfileInfoBox();
    a.show()

    sys.exit(app.exec_())
