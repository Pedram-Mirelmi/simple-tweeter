import sys

from client.BackendPackages.BackendApp import BaseBackendApp
from client.BackendPackages.ClientKeywords import *

from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, \
    QWidget, QGridLayout, QTabWidget, QMenuBar, QStatusBar, QTextEdit
from PyQt5 import QtCore

from client.UIPackages.LoginRegister import LogRegWidget
import client.UIPackages.Widgets.Tabs as Tabs
import client.UIPackages.Widgets.ToolBarMenus as ToolMenus
from client.UIPackages.Widgets.SingleTweet import SingleTweetBox
from client.UIPackages.PopupWindow import popBox


class BaseUIApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(821, 594)
        self.central_widget = QWidget(self)
        self.main_layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def _setupMainUI(self):
        self._setMainTabWidget()
        self._initiateToolBar()

    def _setMainTabWidget(self):
        self.main_tab_widget = QTabWidget(self)
        self.main_tab_widget.setGeometry(QtCore.QRect(0, 0, 801, 570))
        self.main_tab_widget.setMinimumSize(QtCore.QSize(801, 551))
        self.main_layout.addWidget(self.main_tab_widget)
        self.main_tab_widget.setTabsClosable(True)
        self.main_tab_widget.tabCloseRequested.connect(self.closeTab)

    def setMainTabs(self):
        self._setHomeTab()
        self._setSearchTab()
        self._setProfileTab()

    def closeTab(self, currentIndex):
        current_widget = self.main_tab_widget.widget(currentIndex)
        self.main_tab_widget.removeTab(currentIndex)
        current_widget.deleteLater()

    def _setHomeTab(self):
        self.home_tab = Tabs.HomeTab()
        self.main_tab_widget.addTab(self.home_tab, "")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.home_tab), "Home")

    def _setSearchTab(self):
        self.search_tab = Tabs.SearchTab()
        self.main_tab_widget.addTab(self.search_tab, "")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.search_tab), "Search")

    def _setProfileTab(self):
        self.profile_tab = Tabs.ProfileTab()
        self.main_tab_widget.addTab(self.profile_tab, "")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.profile_tab), "Your Profile")

    def _initiateToolBar(self):
        self.tool_bar = QMenuBar(self)
        self.tool_bar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.setMenuBar(self.tool_bar)

        self.action_menu = ToolMenus.ToolBarMenu(self.tool_bar)
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.tool_bar.addAction(self.action_menu.menuAction())


class App(BaseUIApp, BaseBackendApp):
    def __init__(self, port: int = 9999, max_req_len: int = 4):
        BaseUIApp.__init__(self)
        BaseBackendApp.__init__(self, port, max_req_len)
        self.logreg_widget = LogRegWidget(self, self.req_handler)
        self.main_layout.addWidget(self.logreg_widget, 0, 0, 1, 1)
        self.setIntro()

    def setIntro(self):
        self.logreg_widget.register_button.clicked.connect(
            lambda: self.register(self.logreg_widget.reg_user_field.text(),
                                  self.logreg_widget.reg_name_field.text(),
                                  self.logreg_widget.reg_pass_field.text())
        )
        self.logreg_widget.login_button.clicked.connect(
            lambda: self.login(self.logreg_widget.log_user_field.text(),
                               self.logreg_widget.log_pass_field.text())
        )

    def initiateMainEnv(self):
        self.deleteLogReqWindow()
        self.req_handler.setUserInfo(self.user_info)
        self._setupMainUI()
        self.setMainTabs()
        self.addHeaderToHomeTab()
        self.addHeaderToProfileTab()
        self.reload()

    def addHeaderToProfileTab(self):
        self.profile_tab.addProfileInfoHeader(self.user_info)

    def addHeaderToHomeTab(self):
        self.home_tab.addWriteTweetHeader(self.user_info[USERNAME])
        self.home_tab.main_env.header.send_button.clicked.connect(
            lambda: self.writeNewTweet(self.home_tab.main_env.header.tweet_text_field)
        )

    def deleteLogReqWindow(self):
        self.logreg_widget.deleteLater()
        del self.logreg_widget

    def reload(self):
        self.reloadTab(self.home_tab)
        self.reloadTab(self.profile_tab, self.user_info[USER_ID])

    def reloadTab(self, tab: Tabs.TweetsTab, user_id: int = -1):
        tab.clear()
        all_tweets = self.req_handler.allTweets() if user_id == -1 \
            else self.req_handler.userTweets(user_id)
        for tweet_info in all_tweets:
            new_tweet = SingleTweetBox(tab.main_env, tweet_info)
            self.addTweetToTab(new_tweet, tab)
            tab.all_tweets.append(new_tweet)

    def addTweetToTab(self, new_tweet: SingleTweetBox, tab: Tabs.TweetsTab):
        tab.main_env.container.grid.addWidget(
            new_tweet, tab.main_env.row_index, 0, 1, 1)
        tab.main_env.row_index += 1
        new_tweet.box.like_button.clicked.connect(
            lambda: self.likeTweet(new_tweet.info[TWEET_ID])
        )
        new_tweet.box.comment_button.clicked.connect(
            lambda: self.showComments(new_tweet.info[TWEET_ID])
        )

    def showComments(self, tweet_id: int):
        pass

    def likeTweet(self, tweet_id: int):
        response = self._likeTweet(tweet_id)
        if not response[OUTCOME]:
            popBox(title=FAILED, message=f'{response[STATUS]}', Qicon=QMessageBox.Critical,
                   std_buttons=[QMessageBox.Ok])
        else:
            self.reloadTab(self.main_tab_widget.currentWidget())

    def login(self, username: str, password: str):
        response = self._login(username, password)
        if response[OUTCOME]:
            popBox(title=SUCCESS, message='You successfully logged in!',
                   Qicon=QMessageBox.Information, std_buttons=[QMessageBox.Ok])
            self.user_info = response
            self.initiateMainEnv()
        else:
            popBox(title=FAILED, message=response[STATUS],
                   Qicon=QMessageBox.Critical, std_buttons=[QMessageBox.Ok])

    def register(self, username: str, name: str, password: str):
        response = self._register(username, name, password)
        if response[OUTCOME]:
            popBox(title=SUCCESS, message='You successfully registered!',
                   Qicon=QMessageBox.Information, std_buttons=[QMessageBox.Ok])
            self.user_info = response
            self.initiateMainEnv()
        else:
            popBox(title=FAILED, message=response[STATUS],
                   Qicon=QMessageBox.Critical, std_buttons=[QMessageBox.Ok])

    def writeNewTweet(self, tweet_text_field: QTextEdit):
        response = self._writeNewTweet(tweet_text_field.toPlainText())
        if response[OUTCOME]:
            tweet_text_field.clear()
            self.reload()
        else:
            popBox(title=FAILED, message="Couldn't write new tweet!",
                   Qicon=QMessageBox.Critical, std_buttons=QMessageBox.Ok)

    def __del__(self):
        self.req_handler.terminate()


if __name__ == "__main__":
    qt_app = QApplication(sys.argv)

    window = App(port=9990)
    window.show()

    sys.exit(qt_app.exec_())
