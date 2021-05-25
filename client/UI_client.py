import sys

from client.BackendPackages.BackendApp import BaseBackendApp
from client.BackendPackages.ClientKeywords import *

from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QGridLayout, QTabWidget, QMenuBar, \
    QStatusBar
from PyQt5 import QtCore

from client.UIPackages.LoginRegister import LogRegWidget
import client.UIPackages.Widgets.Tabs as Tabs
import client.UIPackages.Widgets.ToolBarMenus as ToolMenus
from client.UIPackages.Widgets.SingleTweet import SingleTweetBox
from client.UIPackages.Widgets.WriteTweet import WriteTweetBox
from client.UIPackages.Widgets.ManyTweet import ManyTweetBox


class BaseUIApp(QMainWindow):
    def __init__(self):
        super().__init__()
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
    def __init__(self, port: int = 9990, max_req_len: int = 4):
        BaseUIApp.__init__(self)
        BaseBackendApp.__init__(self, port, max_req_len)
        self.logreg_widget = LogRegWidget(self)
        self.main_layout.addWidget(self.logreg_widget, 0, 0, 1, 1)
        self.initiateIntro()

    def __setFuncs(self):
        SingleTweetBox.likeFunc = self.likeTweet
        WriteTweetBox.sendButtonFunc = self.writeNewTweet
        ManyTweetBox.tweetCatcher = self._getAllTweet

    def initiateIntro(self):
        LogRegWidget.login_button_func = self.login
        LogRegWidget.register_button_func = self.register

    def __initiateMainEnv(self):
        self.logreg_widget.deleteLater()
        del self.logreg_widget
        self.req_handler.setUserInfo(self.user_info)
        self.__setFuncs()
        self._setupMainUI()
        self.setMainTabs()
        print(self.user_info)
        self.home_tab.addWriteTweetHeader(self.user_info[USERNAME])

    def login(self, username: str, password: str):
        res = self._login(username, password)
        if res[OUTCOME]:
            self.popBox(title=SUCCESS, message='You successfully logged in!',
                        Qicon=QMessageBox.Information, std_buttons=[QMessageBox.Ok])
            self.user_info = res
            self.__initiateMainEnv()
        else:
            self.popBox(title=FAILED, message=res[STATUS],
                        Qicon=QMessageBox.Critical, std_buttons=[QMessageBox.Ok])

    def register(self, username: str, name: str, password: str):
        res = self._register(username, name, password)
        if res[OUTCOME]:
            self.popBox(title=SUCCESS, message='You successfully registered!',
                        Qicon=QMessageBox.Information, std_buttons=[QMessageBox.Ok])
            self.user_info = res
            self.__initiateMainEnv()
        else:
            self.popBox(title=FAILED, message=res[STATUS],
                        Qicon=QMessageBox.Critical, std_buttons=[QMessageBox.Ok])

    def likeTweet(self, tweet_id: int):
        return self._likeTweet(tweet_id)

    def writeNewTweet(self, tweet_text: str):
        response = self._writeNewTweet(tweet_text)[OUTCOME]

    @staticmethod
    def popBox(title: str, message: str, Qicon: int, std_buttons: list[int]):
        res = 0
        for num in std_buttons:
            res = res | num
        popup_window = QMessageBox(text=message)
        popup_window.setWindowTitle(title)
        popup_window.setIcon(Qicon)
        popup_window.setStandardButtons(res)
        popup_window.exec_()


if __name__ == "__main__":
    qt_app = QApplication(sys.argv)

    a = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(qt_app.exec_())
