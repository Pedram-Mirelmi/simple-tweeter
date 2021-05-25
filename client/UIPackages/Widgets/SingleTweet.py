import sys

from typing import Union, Iterable

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, \
    QTextBrowser, QPushButton, QScrollArea, QApplication, QMessageBox

from client.BackendPackages.ClientKeywords import *


def popBox(title: str, message: str, icon: int, std_buttons: Iterable[int]):
    res = 0
    for num in std_buttons:
        res = res | num
    popup_window = QMessageBox(text=message)
    popup_window.setWindowTitle(title)
    popup_window.setIcon(icon)
    popup_window.setStandardButtons(res)
    popup_window.exec_()


class SingleTweetContainer(QWidget):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(0, 0, 448, 248))
        self.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.__setupUi()

    def __setupUi(self):
        self.__setupUsername()
        self.__setupTimeField()
        self.__setupTweetTextField()
        self.__setupLikeButton()
        self.__setupCommentButton()

    def __setupUsername(self):
        self.username_field = QPushButton(self)
        self.username_field.setObjectName("username_field")
        self.gridLayout.addWidget(self.username_field, 0, 0, 1, 1)

    def __setupTimeField(self):
        self.time_label = QLabel(self)
        self.time_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.time_label.setObjectName("time_field")
        self.gridLayout.addWidget(self.time_label, 0, 3, 1, 1)

    def __setupTweetTextField(self):
        self.tweet_text_field = QTextBrowser(self)
        self.tweet_text_field.setObjectName("tweet_text_field")
        self.gridLayout.addWidget(self.tweet_text_field, 1, 0, 1, 4)

    def __setupLikeButton(self):
        self.like_button = QPushButton(self)
        self.like_button.setObjectName("like_button")
        self.gridLayout.addWidget(self.like_button, 2, 0, 1, 1)

    def __setupCommentButton(self):
        self.comment_button = QPushButton(self)
        self.comment_button.setObjectName("Comment_button")
        self.gridLayout.addWidget(self.comment_button, 2, 1, 1, 1)
        self.initiateTexts()

    def initiateTexts(self):
        _translate = QtCore.QCoreApplication.translate
        self.username_field.setText("usernameField")
        self.time_label.setText("timeField")
        self.like_button.setText("Like")
        self.comment_button.setText("Comment")


class SingleTweetBox(QScrollArea):
    likeFunc: callable

    def __init__(self, mother_area: QWidget = None, reloader: callable = None):
        super().__init__(mother_area)
        self.reloader = reloader
        self.setGeometry(QtCore.QRect(0, 10, 450, 250))
        self.setMinimumSize(QtCore.QSize(450, 250))
        self.setMaximumSize(QtCore.QSize(450, 250))
        self.setWidgetResizable(True)
        self.tweet_id = -1
        self.setObjectName("tweet_box")
        self.box = SingleTweetContainer(self)
        self.setWidget(self.box)

    def initiateTweet(self, tweet_info: dict[str, Union[str, int]]):
        self.tweet_id = tweet_info[TWEET_ID]
        self.box.username_field.setText(tweet_info[USERNAME])
        self.box.time_label.setText(tweet_info[CREATED_AT])
        self.box.tweet_text_field.setText(tweet_info[TWEET_TEXT])
        self.box.like_button.setText(f"Like({tweet_info[LIKES]})")
        self.__setButtons()

    def __setButtons(self):
        self.box.like_button.clicked.connect(self.likeClicked)
        self.box.comment_button.clicked.connect(self.commentClicked)

    def likeClicked(self):
        res = self.likeFunc(self.tweet_id)
        if res[OUTCOME]:
            self.reloader()
        else:
            popBox(title=FAILED, message=f'{res[STATUS]}', icon=QMessageBox.Critical,
                   std_buttons=[QMessageBox.Ok])

    def commentClicked(self):
        print('comment button clicked!')


if __name__ == "__main__":
    class Window(QWidget):
        def __init__(self):
            super().__init__()
            self.grid = QGridLayout(self)
            self.grid.addWidget(SingleTweetBox(), 1, 1)
            self.grid.addWidget(SingleTweetBox(), 2, 1)


    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
