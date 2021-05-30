from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QWidget

class ToolBar(QMenuBar):
    def __init__(self, main_window: QMainWindow):
        super().__init__(main_window)
        self.main_window = main_window
        self.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.main_window.setMenuBar(self)
        self.statusbar = QtWidgets.QStatusBar(self.main_window)
        self.main_window.setStatusBar(self.statusbar)
        self.tabs_menu = QtWidgets.QMenu(self)
        self._createActions()
        self._initiateTexts()

    def _createActions(self):
        self.reload_current = QtWidgets.QAction(self.main_window)
        self.reload_all = QtWidgets.QAction(self.main_window)
        self.home_tab_opener = QtWidgets.QAction(self.main_window)
        self.search_tab_opener = QtWidgets.QAction(self.main_window)
        self.profile_tab_opener = QtWidgets.QAction(self.main_window)
        self.close_current = QtWidgets.QAction(self.main_window)
        self.exit = QtWidgets.QAction(self.main_window)
        self._addActions()

    def _addActions(self):
        self.tabs_menu.addAction(self.home_tab_opener)
        self.tabs_menu.addAction(self.search_tab_opener)
        self.tabs_menu.addAction(self.profile_tab_opener)
        self.tabs_menu.addAction(self.reload_current)
        self.tabs_menu.addAction(self.reload_all)
        self.tabs_menu.addAction(self.close_current)
        self.tabs_menu.addAction(self.exit)
        self.addAction(self.tabs_menu.menuAction())

    def _initiateTexts(self):
        self.tabs_menu.setTitle("Tabs")
        self.reload_current.setText("Reload Current")
        self.reload_current.setStatusTip("Reload Current Tab")
        self.reload_current.setShortcut("Ctrl+Shift+R")
        self.reload_all.setText("Reload All")
        self.reload_all.setStatusTip("Reload All Tabs")
        self.reload_all.setShortcut("Ctrl+R")
        self.home_tab_opener.setText("Home")
        self.home_tab_opener.setStatusTip("Open home tab if needed")
        self.home_tab_opener.setShortcut("Ctrl+H")
        self.search_tab_opener.setText("Search")
        self.search_tab_opener.setStatusTip("Open search tab if needed")
        self.search_tab_opener.setShortcut("Ctrl+S")
        self.profile_tab_opener.setText("Profile")
        self.profile_tab_opener.setStatusTip("Open your profile tab if needed")
        self.profile_tab_opener.setShortcut("Ctrl+P")
        self.close_current.setText("Close Current")
        self.close_current.setStatusTip("Close Current Tab")
        self.close_current.setShortcut("Ctrl+W")
        self.exit.setText("Exit")
        self.exit.setStatusTip("Exit programm")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = QMainWindow()
    w = ToolBar(win)
    win.show()
    sys.exit(app.exec_())

