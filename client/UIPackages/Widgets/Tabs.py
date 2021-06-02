from typing import Union

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QListView, QLabel, QScrollArea, QGridLayout

from client.BackendPackages import ClientKeywords
from .ManyTweet import MultiTweetBox
from .Boxes import SingleTweetBox, SingleCommentBox
from .Headers import ProfileInfoHeader, WriteItemHeader


class SearchTab(QScrollArea):
    def __init__(self):
        super(SearchTab, self).__init__()
        self.setWidgetResizable(True)
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


class MultiItemTab(QWidget):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.grid = QGridLayout(self)
        self.main_env = MultiTweetBox(self)
        self.grid.addWidget(self.main_env, 0, 0, 1, 1)
        self.all_items = []

    def clearItems(self):
        self.all_items: list[SingleCommentBox]
        while self.all_items:
            try:
                tweet = self.all_items.pop()
                tweet.deleteLater()
                del tweet
            except:
                pass
        self.main_env.row_index = 1

    def __del__(self):
        self.all_items: list[QWidget]
        for item in self.all_items:
            try:
                item.deleteLater()
                del item
            except:
                pass


class CommentTab(MultiItemTab):
    def __init__(self, tweet_info: dict[str, str], username: str):
        super().__init__()
        self.setTweetHeader(tweet_info)
        self.setWriteCommentHeader(username)

    def clearItems(self):
        super(CommentTab, self).clearItems()
        self.main_env.row_index = 2

    def setTweetHeader(self, tweet_info: dict[str, str]):
        self.tweet_header = SingleTweetBox(self.main_env, tweet_info)
        self.main_env.setHeader(self.tweet_header)

    def setWriteCommentHeader(self, username: str):
        self.write_comment_header = WriteItemHeader(self, 'Comment')
        self.write_comment_header.initiateTexts(username)
        self.main_env.container.grid.addWidget(self.write_comment_header, self.main_env.row_index, 0, 1, 1)
        self.main_env.row_index += 1


class HomeTab(MultiItemTab):
    def __init__(self, mother_are: QWidget):
        super(HomeTab, self).__init__(mother_are)

    def addWriteTweetHeader(self, username: str):
        self.header = WriteItemHeader(self.main_env.container, 'Tweet')
        self.header.initiateTexts(username)
        self.main_env.setHeader(self.header)

    def updateHeader(self, username: str):
        self.header.setTitle(f"Write Tweet as {username}")


class ProfileTab(MultiItemTab):
    def __init__(self):
        super().__init__()

    def addProfileInfoHeader(self, user_info: dict[str, str]):
        self.header = ProfileInfoHeader(self.main_env.container)
        self.header.initiateTexts(user_info)
        self.main_env.setHeader(self.header)

    def updateHeader(self, profile_info: dict[str, str]):
        self.header.initiateTexts(profile_info)


if __name__ == "__main__":
    import sys
