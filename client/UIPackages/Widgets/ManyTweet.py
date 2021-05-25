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

    def __init__(self, mother_area: QWidget = None, reloader: callable = None):
        super().__init__(mother_area)
        self.reloader = reloader
        self.t_container = ManyTweetContainer()
        self.setWidget(self.t_container)
        self.setWidgetResizable(True)
        self.row_index = 1

    def updateAllTweets(self, all_tweets: list[dict[str, str]] = None):
        all_tweets = self.tweetCatcher()
        self.row_index = 1
        for tweet in all_tweets:
            self.addSingleTweet(tweet)

    def addWriteTweetHeader(self, username: str):
        self.header = WriteTweetBox(self.t_container, self.updateAllTweets)
        self.header.initiateBox(username)
        self.t_container.grid.addWidget(self.header, 0, 0, 1, 1)

    def addProfileInfoHeader(self, profile_info: dict[str, str]):  # TODO
        pass

    def addSingleTweet(self, tweet_info: dict[str, str]):
        new_tweet = SingleTweetBox(self.t_container, self.updateAllTweets)
        new_tweet.initiateTweet(tweet_info)
        self.t_container.grid.addWidget(new_tweet, self.row_index, 0, 1, 1)
        self.row_index += 1


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    sys.exit(app.exec_())
