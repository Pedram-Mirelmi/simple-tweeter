import sys

sys.path.insert(1, '/home/pedram/PycharmProjects/my-project/client')
sys.path.insert(1, '/home/pedram/PycharmProjects/my-project/')

from client.BackendPackages.BackendApp import BaseBackendApp
from client.BackendPackages.ClientKeywords import *

from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QGridLayout, QTabWidget
from PyQt5 import QtCore

from client.UIPackages.LoginRegister import LogRegWidget
import client.UIPackages.Widgets.Tabs as Tabs
from client.UIPackages.Widgets.SingleTweet import SingleTweetBox
from client.UIPackages.Widgets.WriteTweet import WriteTweetBox
from client.UIPackages.Widgets.ManyTweet import ManyTweetBox


class BaseApp(QMainWindow, BaseBackendApp):
    def __init__(self, port: int = 9990, max_req_len: int = 4):
        QMainWindow.__init__(self)
        BaseBackendApp.__init__(self, port=port, max_req_len=max_req_len)
        self.resize(821, 594)
        self.central_widget = QWidget(self)
        self.main_layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def _setupMainUI(self):
        self._setMainTabWidget()
        self._initiateTexts()

    def _setMainTabWidget(self):
        self.main_tab_widget = QTabWidget(self)
        self.main_tab_widget.setGeometry(QtCore.QRect(10, 0, 801, 570))
        self.main_tab_widget.setMinimumSize(QtCore.QSize(801, 551))
        self.home_tab = Tabs.HomeTab()
        self.search_tab = Tabs.SearchTab()
        self.profile_tab = Tabs.ProfileTab()
        self.main_tab_widget.addTab(self.home_tab, "")
        self.main_tab_widget.addTab(self.search_tab, "")
        self.main_tab_widget.addTab(self.profile_tab, "")
        self.main_layout.addWidget(self.main_tab_widget)

    def _initiateTexts(self):
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.home_tab), "Home")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.search_tab), "Search")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.profile_tab), "Your Profile")


class App(BaseApp):
    def __init__(self, port: int = 9990, max_req_len: int = 4):
        super().__init__(port=port, max_req_len=max_req_len)
        self.logreg_widget = LogRegWidget(self)
        self.main_layout.addWidget(self.logreg_widget, 0, 0, 1, 1)
        self.initiateIntro()

    def __setFuncs(self):
        SingleTweetBox.likeFunc = self._likeTweet
        WriteTweetBox.sendButtonFunc = self._writeNewTweet
        ManyTweetBox.tweetCatcher = self._getAllTweet

    def initiateIntro(self):
        LogRegWidget.login_button_func = self.login
        LogRegWidget.register_button_func = self.register

    def __initiateMainEnv(self):
        self.logreg_widget.deleteLater()
        del self.logreg_widget
        self.__setFuncs()
        self._setupMainUI()
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
