import sys

sys.path.insert(1, '/home/pedram/PycharmProjects/my-project/')
sys.path.insert(1, '/home/pedram/PycharmProjects/my-project/client')

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QScrollArea, QGridLayout, QApplication
from .WriteTweet import WriteTweetBox
from .SingleTweet import SingleTweetBox


class ManyTweetContainer(QWidget):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.setGeometry(QtCore.QRect(0, 0, 629, 859))
        self.grid = QGridLayout(self)


class ManyTweetBox(QScrollArea):
    tweetCatcher: callable
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.t_container = ManyTweetContainer()
        self.setWidget(self.t_container)
        self.setWidgetResizable(True)
        self.row_index = 1

    def updateAllTweets(self):
        self.row_index = 1
        all_tweets = self.tweetCatcher()
        for tweet in all_tweets:
            self.addSingleTweet(tweet)

    def addWriteTweetHeader(self, username: str):
        self.header = WriteTweetBox(mother_area=self.t_container, username=username)
        self.t_container.grid.addWidget(self.header, 0, 0, 1, 1)

    def addProfileInfoHeader(self, profile_info: dict[str, str]):  # TODO
        pass

    def addSingleTweet(self, tweet_info: dict[str, str]):
        new_tweet = SingleTweetBox(self.t_container)
        new_tweet.initiateTweet(tweet_info)
        self.t_container.grid.addWidget(new_tweet, self.row_index, 0, 1, 1)
        self.row_index += 1


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    sys.exit(app.exec_())
