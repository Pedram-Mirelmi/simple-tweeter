from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, \
    QTextBrowser, QPushButton, QScrollArea, QApplication


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
        self.username_field = QLabel(self)
        self.username_field.setObjectName("username_field")
        self.gridLayout.addWidget(self.username_field, 0, 0, 1, 2)

    def __setupTimeField(self):
        self.time_field = QLabel(self)
        self.time_field.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.time_field.setObjectName("time_field")
        self.gridLayout.addWidget(self.time_field, 0, 2, 1, 1)

    def __setupTweetTextField(self):
        self.tweet_text_field = QTextBrowser(self)
        self.tweet_text_field.setObjectName("tweet_text_field")
        self.gridLayout.addWidget(self.tweet_text_field, 1, 0, 1, 3)

    def __setupLikeButton(self):
        self.like_button = QPushButton(self)
        self.like_button.setObjectName("like_button")
        self.gridLayout.addWidget(self.like_button, 2, 0, 1, 1)

    def __setupCommentButton(self):
        self.Comment_button = QPushButton(self)
        self.Comment_button.setObjectName("Comment_button")
        self.gridLayout.addWidget(self.Comment_button, 2, 1, 1, 1)
        self.initiateTexts()

    def initiateTexts(self):
        _translate = QtCore.QCoreApplication.translate
        self.username_field.setText("usernameField")
        self.time_field.setText("timeField")
        self.like_button.setText("Like")
        self.Comment_button.setText("Comment")


class SingleTweetBox(QScrollArea):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(0, 10, 450, 250))
        self.setMinimumSize(QtCore.QSize(450, 250))
        self.setMaximumSize(QtCore.QSize(450, 250))
        self.setWidgetResizable(True)
        self.setObjectName("tweet_box")
        self.box = SingleTweetContainer(self)
        self.setWidget(self.box)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout(self)
        self.grid.addWidget(SingleTweetBox(), 1, 1)
        self.grid.addWidget(SingleTweetBox(), 2, 1)


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
