import sys
from client.BackendPackages.BackendApp import BaseBackendApp
from client.BackendPackages.ClientKeywords import *

from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, \
    QWidget, QGridLayout, QTabWidget, QTextEdit
from PyQt5 import QtCore

from client.UIPackages.LoginRegister import LogRegWidget
import client.UIPackages.Widgets.Tabs as Tabs
from client.UIPackages.Widgets.ToolBar import ToolBar
from client.UIPackages.Widgets.Boxes import SingleTweetBox, SingleCommentBox
from client.UIPackages.PopupWindow import popBox
from client.UIPackages.SettingsWindow import SettingsWindow


class BaseUIApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(821, 594)
        self.central_widget = QWidget(self)
        self.main_layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def initiateMainUI(self):
        self._setMainTabWidget()
        self.setToolBar()

    def _setMainTabWidget(self):
        self.main_tab_widget = QTabWidget(self)
        self.main_tab_widget.setGeometry(QtCore.QRect(0, 0, 801, 570))
        self.main_tab_widget.setMinimumSize(QtCore.QSize(801, 551))
        self.main_layout.addWidget(self.main_tab_widget)
        self.main_tab_widget.setTabsClosable(True)
        self.main_tab_widget.tabCloseRequested.connect(self.closeTab)

    def closeTab(self, currentIndex):
        current_tab = self.main_tab_widget.widget(currentIndex)
        print(f"deleting {current_tab}")
        self.main_tab_widget.removeTab(currentIndex)
        current_tab.deleteLater()
        current_tab.setParent(None)
        del current_tab

    def setHomeTab(self, index: int = 0):
        self.home_tab = Tabs.HomeTab(self)
        self.main_tab_widget.insertTab(index, self.home_tab, "")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.home_tab), "Home")

    def setSearchTab(self, index: int = 1):
        self.search_tab = Tabs.SearchTab()
        self.main_tab_widget.insertTab(index, self.search_tab, "")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.search_tab), "Search")

    def setProfileTab(self, index: int = 2):
        self.profile_tab = Tabs.ProfileTab()
        self.main_tab_widget.insertTab(index, self.profile_tab, "")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.profile_tab), "Your Profile")

    def setToolBar(self):
        self.tool_bar = ToolBar(self)


class App(BaseUIApp, BaseBackendApp):
    def __init__(self, port: int = 9999, max_req_len: int = 5):
        BaseUIApp.__init__(self)
        BaseBackendApp.__init__(self, port, max_req_len)
        self.logreg_widget = LogRegWidget(self, self.req_handler)
        self.main_layout.addWidget(self.logreg_widget, 0, 0, 1, 1)
        self.setIntro()
        self.settings_window = SettingsWindow(self.req_handler, self.user_info)

    def setIntro(self):
        self.logreg_widget.register_button.clicked.connect(
            lambda: self.register(self.logreg_widget.reg_user_field.text().strip(),
                                  self.logreg_widget.reg_name_field.text().strip(),
                                  self.logreg_widget.reg_pass_field.text())
        )
        self.logreg_widget.login_button.clicked.connect(
            lambda: self.login(self.logreg_widget.log_user_field.text().strip(),
                               self.logreg_widget.log_pass_field.text())
        )

    def deleteIntro(self):
        self.logreg_widget.deleteLater()
        del self.logreg_widget

    def initiateMainEnv(self):
        self.deleteIntro()
        self.req_handler.setUserInfo(self.user_info)
        self.initiateMainUI()
        self.setTabs()
        self.reload()

    def setToolBar(self):
        super(App, self).setToolBar()
        self.tool_bar.reload_current.triggered.connect(
            lambda: self.reloadTab(self.main_tab_widget.currentWidget())
        )
        self.tool_bar.reload_all.triggered.connect(
            self.reload
        )
        self.tool_bar.close_current.triggered.connect(
            lambda: self.closeTab(self.main_tab_widget.currentIndex())
        )
        self.tool_bar.home_tab_opener.triggered.connect(
            self.checkHomeTab
        )
        self.tool_bar.search_tab_opener.triggered.connect(
            self.checkSearchTab
        )
        self.tool_bar.profile_tab_opener.triggered.connect(
            self.checkProfileTab
        )
        self.tool_bar.setting_action.triggered.connect(
            self.openSettingsWindow
        )

    def openSettingsWindow(self):
        self.settings_window.initiateFields(self.user_info)
        self.settings_window.show()

    def setTabs(self):
        self.setHomeTab()
        self.setSearchTab()
        self.setProfileTab()

    def setHomeTab(self, index: int = 0):
        super(App, self).setHomeTab()
        self.home_tab.addWriteTweetHeader(self.user_info[USERNAME])
        self.home_tab.main_env.header.send_button.clicked.connect(
            lambda: self.writeNewTweet(self.home_tab.main_env.header.item_text_field)
        )

    def checkHomeTab(self):
        try:
            self.main_tab_widget.setCurrentWidget(self.home_tab)
        except:
            self.setHomeTab()
            self.reloadTab(self.home_tab)
            self.main_tab_widget.setCurrentWidget(self.home_tab)

    def setSearchTab(self, index: int = 1):
        super(App, self).setSearchTab()
        # TODO complete search tab

    def checkSearchTab(self):
        try:
            self.main_tab_widget.setCurrentWidget(self.search_tab)
        except:
            self.setSearchTab()
            self.reloadTab(self.search_tab)
            self.main_tab_widget.setCurrentWidget(self.search_tab)

    def setProfileTab(self, index: int = 2):
        super(App, self).setProfileTab()
        self.profile_tab.addProfileInfoHeader(self.user_info)

    def checkProfileTab(self):
        try:
            self.main_tab_widget.setCurrentWidget(self.profile_tab)
        except:
            self.setProfileTab()
            self.reloadTab(self.profile_tab)
            self.main_tab_widget.setCurrentWidget(self.profile_tab)

    def reload(self):
        for tab_index in range(self.main_tab_widget.count()):
            self.reloadTab(self.main_tab_widget.widget(tab_index))

    def reloadTab(self, tab: QWidget):
        if isinstance(tab, Tabs.SearchTab):
            self.reloadSearchTab(tab)
        elif isinstance(tab, Tabs.CommentTab):
            self.reloadCommentTab(tab)
        elif isinstance(tab, Tabs.HomeTab):
            self.reloadHomeTab()
        elif isinstance(tab, Tabs.ProfileTab):
            self.reloadProfileTab()

    @staticmethod
    def reloadSearchTab(tab: Tabs.SearchTab):  # TODO
        tab.search_field.clear()

    def reloadHomeTab(self):
        self.home_tab.updateHeader(self.user_info[USERNAME])
        self.reloadTweetsInTab(self.home_tab, self.req_handler.getAllTweets())

    def reloadProfileTab(self,):
        self.profile_tab.updateHeader(self.user_info)
        self.reloadTweetsInTab(self.profile_tab, self.req_handler.userTweets(self.user_info[USER_ID]))

    def reloadCommentTab(self, tab: Tabs.CommentTab):
        tab.tweet_header.initiateTexts(self.req_handler.getTweetInfo(tab.tweet_header.info[TWEET_ID]))
        tab.write_comment_header.initiateTexts(self.user_info[USERNAME])
        self.reloadCommentsInTab(tab)

    def reloadTweetsInTab(self, tab: Tabs.MultiItemTab, all_tweets: list[dict]):
        tab.clearItems()
        for tweet_info in all_tweets:
            new_tweet = SingleTweetBox(tab.main_env, tweet_info)
            self.appendItemToTab(tab, new_tweet)
            self.setTweetButtons(new_tweet)
            tab.all_items.append(new_tweet)

    def setTweetButtons(self, tweet: SingleTweetBox):
        tweet.box.like_button.clicked.connect(
            lambda: self.likeTweet(tweet.info[TWEET_ID])
        )
        tweet.box.comment_button.clicked.connect(
            lambda: self.showComments(tweet.info)
        )

    def setCommentButtons(self, comment: SingleCommentBox):
        comment.box.like_button.clicked.connect(
            lambda: self.likeComment(comment.info[COMMENT_ID])
        )

    def reloadCommentsInTab(self, tab):
        tab.clearItems()
        tab.main_env.row_index = 2
        all_comments = self.req_handler.getComments(tab.tweet_header.info[TWEET_ID])
        for comment_info in all_comments:
            new_comment = SingleCommentBox(tab.main_env, comment_info)
            self.appendItemToTab(tab, new_comment)
            self.setCommentButtons(new_comment)
            tab.all_items.append(new_comment)
            
    def showComments(self, tweet_info: dict[str, str]):
        new_tab = Tabs.CommentTab(tweet_info, self.user_info[USERNAME])
        new_tab.write_comment_header.send_button.clicked.connect(
            lambda: self.writeNewComment(
                new_tab.write_comment_header.item_text_field,
                tweet_info[TWEET_ID])
        )
        self.main_tab_widget.insertTab(self.main_tab_widget.currentIndex() + 1, new_tab, "")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(new_tab), "Comments")
        self.main_tab_widget.setCurrentWidget(new_tab)
        self.reloadCommentsInTab(new_tab)
        self.setTweetButtons(new_tab.tweet_header)

    @staticmethod
    def appendItemToTab(tab: Tabs.MultiItemTab, item: QWidget):
        tab.main_env.container.grid.addWidget(
            item, tab.main_env.row_index, 0, 1, 1)
        tab.main_env.row_index += 1

    def likeTweet(self, tweet_id: int):
        response = self._likeTweet(tweet_id)
        if not response[OUTCOME]:
            popBox(title=FAILED, message=f'{response[STATUS]}', Qicon=QMessageBox.Critical,
                   std_buttons=[QMessageBox.Ok])
        else:
            self.reload()

    def likeComment(self, comment_id: int):
        response = self._likeComment(comment_id)
        if not response[OUTCOME]:
            popBox(title=FAILED, message=f'{response[STATUS]}', Qicon=QMessageBox.Critical,
                   std_buttons=[QMessageBox.Ok])
        else:
            self.reload()

    def login(self, username: str, password: str):
        response = self._login(username, password)
        if response[OUTCOME]:
            popBox(title=SUCCESS, message='You successfully logged in!',
                   Qicon=QMessageBox.Information, std_buttons=[QMessageBox.Ok])
            print(f"response:{response}")
            self.user_info.update(response)
            self.initiateMainEnv()
        else:
            popBox(title=FAILED, message=response[STATUS],
                   Qicon=QMessageBox.Critical, std_buttons=[QMessageBox.Ok])

    def register(self, username: str, name: str, password: str):
        if username and password:
            response = self._register(username, name, password)
            if response[OUTCOME]:
                popBox(title=SUCCESS, message='You successfully registered!',
                       Qicon=QMessageBox.Information, std_buttons=[QMessageBox.Ok])
                self.user_info.update(response)
                self.initiateMainEnv()
            else:
                popBox(title=FAILED, message=response[STATUS],
                       Qicon=QMessageBox.Critical, std_buttons=[QMessageBox.Ok])

    def writeNewTweet(self, tweet_text_field: QTextEdit):
        if tweet_text_field.toPlainText():
            response = self._writeNewTweet(tweet_text_field.toPlainText().strip())
            if response[OUTCOME]:
                tweet_text_field.clear()
                self.reload()
            else:
                popBox(title=FAILED, message="Couldn't write new tweet!",
                       Qicon=QMessageBox.Critical, std_buttons=QMessageBox.Ok)

    def writeNewComment(self, comment_text_field: QTextEdit, tweet_id: int):
        if comment_text_field.toPlainText():
            response = self._writeNewComment(comment_text_field.toPlainText().strip(), tweet_id)
            if response[OUTCOME]:
                comment_text_field.clear()
                self.reload()
            else:
                popBox(title=FAILED, message="Couldn't write new tweet!",
                       Qicon=QMessageBox.Critical, std_buttons=QMessageBox.Ok)

    def __del__(self):
        self.req_handler.terminate()


if __name__ == "__main__":
    qt_app = QApplication(sys.argv)

    window = App()
    window.show()

    qt_app.exec_()
    sys.exit()
