from typing import Union

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QListView, QLabel, QApplication, QGridLayout

import sys

sys.path.insert(1, '/home/pedram/PycharmProjects/my-project/')
sys.path.insert(1, '/home/pedram/PycharmProjects/my-project/client')

from client.BackendPackages import ClientKeywords
from .ManyTweet import ManyTweetBox


class SearchTab(QWidget):
    def __init__(self):
        super(SearchTab, self).__init__()
        self.search_field = QLineEdit(self)
        self.search_field.setGeometry(QtCore.QRect(73, 10, 231, 25))
        self.search_button = QPushButton(self)
        self.search_button.setGeometry(QtCore.QRect(3, 10, 65, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.search_button.setFont(font)
        # set the result box
        self.search_result_list = QListView(self)
        self.search_result_list.setGeometry(QtCore.QRect(0, 40, 797, 471))
        self.search_result_label = QLabel(self)
        self.search_result_label.setGeometry(QtCore.QRect(646, 10, 141, 20))
        self.__initiateTexts()

    def __initiateTexts(self):
        self.search_button.setText("search:")
        self.search_result_label.setText("Found nothing!")

    def goToProfile(self):  # TODO
        pass


class HomeTab(QWidget):
    tweetCatcher: callable

    def __init__(self):
        super(HomeTab, self).__init__()
        self.grid = QGridLayout(self)
        self.main_env = ManyTweetBox(self)
        self.grid.addWidget(self.main_env, 0, 0, 1, 1)
        self.updateTweets()

    def addWriteTweetHeader(self, username: str):
        self.main_env.addWriteTweetHeader(username)

    def updateTweets(self):
        self.main_env.updateAllTweets()


class ProfileTab(QWidget):
    def __init__(self):
        super(ProfileTab, self).__init__()


if __name__ == "__main__":
    import sys
