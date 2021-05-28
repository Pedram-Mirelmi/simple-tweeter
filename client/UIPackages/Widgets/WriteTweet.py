from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QWidget, QGridLayout, QPushButton, QTextEdit


class WriteTweetBox(QGroupBox):
    sendButtonFunc: callable

    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(270, 40, 450, 244))
        self.setMinimumSize(QtCore.QSize(450, 244))
        self.setMaximumSize(QtCore.QSize(450, 250))

    def initiateBox(self, username):
        self.gridLayout = QGridLayout(self)
        self.tweet_text_field = QTextEdit(self)
        self.gridLayout.addWidget(self.tweet_text_field, 0, 0, 1, 1)
        self.send_button = QPushButton(self)
        self.gridLayout.addWidget(self.send_button, 1, 0, 1, 1)
        self.__initiateTexts(username)

    def __initiateTexts(self, username: str):
        self.setTitle(f"Write Tweet as '{username}':")
        self.send_button.setText("Send")
