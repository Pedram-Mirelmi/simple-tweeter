from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QWidget, QMainWindow, QTabWidget, \
    QLineEdit, QListView, QLabel, QApplication, QGridLayout

from .Widgets.ManyTweet import ManyTweetBox

class BaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(821, 594)
        self.central_widget = QWidget(self)
        self.main_layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        # self.__setMainTabWidget()
        # self.__initiateTexts()
        # self.setMinimumSize(QtCore.QSize(821, 594))
        # self.setMaximumSize(QtCore.QSize(821, 594))


    def _setMainTabWidget(self):
        self.main_tab_widget = QTabWidget(self)
        self.main_tab_widget.setGeometry(QtCore.QRect(10, 0, 801, 570))
        self.main_tab_widget.setMinimumSize(QtCore.QSize(801, 551))
        self.home_tab = HomeTab()
        self.search_tab = SearchTab()
        self.profile_tab = ProfileTab()
        self.main_tab_widget.addTab(self.home_tab, "")
        self.main_tab_widget.addTab(self.search_tab, "")
        self.main_tab_widget.addTab(self.profile_tab, "")
        self.main_layout.addWidget(self.main_tab_widget)

    def _initiateTexts(self):
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.home_tab), "Home")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.search_tab), "Search")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.profile_tab), "Your Profile")


class SearchTab(QWidget):
    def __init__(self):
        super(SearchTab, self).__init__()
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


class HomeTab(QWidget):
    def __init__(self):
        super(HomeTab, self).__init__()
        self.grid = QGridLayout(self)
        self.main_env = ManyTweetBox(self)
        self.grid.addWidget(self.main_env, 0, 0, 1, 1)


class ProfileTab(QWidget):
    def __init__(self):
        super(ProfileTab, self).__init__()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = BaseApp()
    ui.show()
    sys.exit(app.exec_())
