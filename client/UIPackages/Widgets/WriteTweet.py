from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QWidget, QGridLayout, QTextEdit, QPushButton, QApplication


class WriteTweetBox(QGroupBox):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(270, 40, 450, 244))
        self.setMinimumSize(QtCore.QSize(450, 244))
        self.setMaximumSize(QtCore.QSize(450, 250))
        self.gridLayout = QGridLayout(self)
        self.tweet_text_field = QTextEdit(self)
        self.gridLayout.addWidget(self.tweet_text_field, 0, 0, 1, 1)
        self.pushButton = QPushButton(self)
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.__initiateTexts()

    def __initiateTexts(self):
        self.setTitle("Write Tweet:")
        self.pushButton.setText("send")
