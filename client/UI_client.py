import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

from BackendPackages.ClienKeywords import *
from UIPackages.Widgets.LoginRegister import LogRegWidget
from BackendPackages.RH_client import RequestHandler
from UIPackages.MainWindow import BaseApp


class App(BaseApp):
    def __init__(self, port: int = 9990, max_req_len: int = 4):
        super().__init__()
        self._user_info = {USERNAME: str(), PASSWORD: str()}
        self.req_handler = RequestHandler(port, max_req_len)
        self._max_req_len = max_req_len
        self.logreg_widget = LogRegWidget(self)
        self.main_layout.addWidget(self.logreg_widget, 0, 0, 1, 1)
        self.initiateIntro()

    def initiateIntro(self):
        LogRegWidget.login_button_func = self.login
        LogRegWidget.register_button_func = self.register

    def register(self, username: str, name: str, password: str) -> None:
        response = self.req_handler.register({REQUEST_TYPE: LOGIN,
                                              USERNAME: username,
                                              NAME: name,
                                              PASSWORD: password})
        if not response[OUTCOME]:
            self.popBox(title='FAILED!', message=f'Ridi! {response[STATUS]}',
                        Qicon=QMessageBox.Critical, std_buttons=[QMessageBox.Ok])
        else:
            self._user_info = response
            self.popBox(title='SUCCESS!', message=f'You successfully registered!',
                        Qicon=QMessageBox.Information, std_buttons=[QMessageBox.Ok])
            self.__enterApp()

    def login(self, username: str, password: str) -> None:
        response = self.req_handler.login({REQUEST_TYPE: LOGIN,
                                           USERNAME: username,
                                           PASSWORD: password})
        if not response[OUTCOME]:
            self.popBox(title='FAILED!', message=f'Ridi! {response[STATUS]}',
                        Qicon=QMessageBox.Critical, std_buttons=[QMessageBox.Ok])
        else:
            self._user_info = response
            self.popBox(title='FAILED!', message=f'You successfully logged in!',
                        Qicon=QMessageBox.Information, std_buttons=[QMessageBox.Ok])
            self.__enterApp()

    def __enterApp(self):
        self.logreg_widget.deleteLater()
        del self.logreg_widget
        self._setMainTabWidget()
        self._initiateTexts()

    @staticmethod
    def popBox(title: str, message: str, Qicon: int,  std_buttons: list[int]):
        res = 0
        for num in std_buttons: res = res | num
        popup_window = QMessageBox(text=message)
        popup_window.setWindowTitle(title)
        popup_window.setIcon(Qicon)
        popup_window.setStandardButtons(res)
        popup_window.exec_()

if __name__ == "__main__":
    qt_app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(qt_app.exec_())
