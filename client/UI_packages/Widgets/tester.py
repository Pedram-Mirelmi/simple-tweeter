import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, \
    QTextBrowser, QPushButton, QScrollArea, QApplication, QMainWindow

from SingleTweet import SingleTweetBox
from ManyTweet import ManyTweetBox


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tweet_menu = ManyTweetBox()
        self.setAutoFillBackground(True)
        for i in range(20):
            self.tweet_menu.t_container.grid.addWidget(SingleTweetBox(), i, 0, 1, 1)
        self.setCentralWidget(self.tweet_menu)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = MyWindow()
    win.show()

    sys.exit(app.exec_())
