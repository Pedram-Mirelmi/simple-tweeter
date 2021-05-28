# incomplete and unused (yet) file
from PyQt5.QtWidgets import QMenu, QMenuBar, QAction


class ToolBarMenu(QMenu):
    def __init__(self, main_tool_bar: QMenuBar):
        super().__init__(main_tool_bar)
        self.action_reload = QAction(self)
        self.action_reload.setShortcut("Ctrl+R")
        self.addAction(self.action_reload)
        self.__initiateTexts()

    def __initiateTexts(self):
        self.action_reload.setText("Reload")
        self.action_reload.setToolTip("Reload current tab")




