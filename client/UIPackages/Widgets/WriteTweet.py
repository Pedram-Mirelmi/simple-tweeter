from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QWidget, QGridLayout, QPlainTextEdit, QPushButton, QApplication


class WriteTweetBox(QGroupBox):
    sendButtonFunc: callable

    def __init__(self, username: str, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(270, 40, 450, 244))
        self.setMinimumSize(QtCore.QSize(450, 244))
        self.setMaximumSize(QtCore.QSize(450, 250))
        self.username = username
        self.__initiateBox()

    def __initiateBox(self):
        self.gridLayout = QGridLayout(self)
        self.tweet_text_field = QPlainTextEdit(self)
        self.gridLayout.addWidget(self.tweet_text_field, 0, 0, 1, 1)
        self.send_button = QPushButton(self)
        self.gridLayout.addWidget(self.send_button, 1, 0, 1, 1)
        self.__initiateTexts()
        self.send_button.clicked.connect(
            lambda: self.sendButtonFunc(self.tweet_text_field.text)
        )

    def __initiateTexts(self):
        self.setTitle(f"Write Tweet as '{self.username}':")
        self.send_button.setText("Send")
