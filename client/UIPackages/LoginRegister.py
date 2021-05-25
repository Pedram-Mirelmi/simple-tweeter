from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, \
    QTabWidget, QGridLayout, QLabel, QLineEdit, QApplication

import sys



class BaseLogRegWidget(QTabWidget):
    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        # self.setGeometry(QtCore.QRect(100, 90, 331, 221))
        self.setMinimumSize(QtCore.QSize(331, 221))
        self.setMaximumSize(QtCore.QSize(441, 281))
        self.__setLoginTab()
        self.__setRegisterTab()
        self.__initiateTexts()

    def __setLoginTab(self):
        self.login_tab = QWidget()
        self.login_grid = QGridLayout(self.login_tab)
        # create items:
        self.log_user_field = QLineEdit(self.login_tab)
        self.log_pass_field = QLineEdit(self.login_tab)
        self.login_button = QPushButton(self.login_tab)
        self.forgotten_pass = QPushButton(self.login_tab)
        self.label_log_user_ = QLabel(self.login_tab)
        self.label_log_pass = QLabel(self.login_tab)
        # adding to layout
        self.login_grid.addWidget(self.label_log_user_, 0, 0, 1, 1)
        self.login_grid.addWidget(self.label_log_pass, 1, 0, 1, 1)
        self.login_grid.addWidget(self.log_user_field, 0, 1, 1, 1)
        self.login_grid.addWidget(self.log_pass_field, 1, 1, 1, 1)
        self.login_grid.addWidget(self.login_button, 2, 1, 1, 1)
        self.login_grid.addWidget(self.forgotten_pass, 2, 0, 1, 1)

        self.addTab(self.login_tab, "")

    def __setRegisterTab(self):
        self.register_tab = QWidget()
        self.register_layout = QGridLayout(self.register_tab)
        # create items:
        self.reg_user_field = QLineEdit(self.register_tab)
        self.reg_name_field = QLineEdit(self.register_tab)
        self.reg_pass_field = QLineEdit(self.register_tab)
        self.register_button = QPushButton(self.register_tab)
        self.label_reg_user = QLabel(self.register_tab)
        self.label_reg_name = QLabel(self.register_tab)
        self.label_reg_pass = QLabel(self.register_tab)
        # adding to layout
        self.register_layout.addWidget(self.reg_user_field, 0, 1, 1, 2)
        self.register_layout.addWidget(self.reg_name_field, 1, 1, 1, 2)
        self.register_layout.addWidget(self.reg_pass_field, 3, 1, 1, 2)
        self.register_layout.addWidget(self.register_button, 4, 0, 1, 3)
        self.register_layout.addWidget(self.label_reg_pass, 3, 0, 1, 1)
        self.register_layout.addWidget(self.label_reg_user, 0, 0, 1, 1)
        self.register_layout.addWidget(self.label_reg_name, 1, 0, 1, 1)

        self.addTab(self.register_tab, "")

    def __initiateTexts(self):
        self.forgotten_pass.setText("Forgotten?")
        self.label_log_user_.setText("Username:")
        self.label_log_pass.setText("Password:")
        self.login_button.setText("Login")
        self.setTabText(self.indexOf(self.login_tab), "Login")
        self.label_reg_pass.setText("Password:")
        self.label_reg_user.setText("Username:")
        self.label_reg_name.setText("name:")
        self.register_button.setText("Register")
        self.setTabText(self.indexOf(self.register_tab), "Register")


class LogRegWidget(BaseLogRegWidget):
    login_button_func: callable
    register_button_func: callable

    def __init__(self, mother_area: QWidget = None):
        super().__init__(mother_area)
        self.initiateLogin()
        self.initiateRegister()

    def initiateRegister(self):
        self.register_button.clicked.connect(
            lambda: self.register_button_func(self.reg_user_field.text(),
                                              self.reg_name_field.text(),
                                              self.reg_pass_field.text())
        )

    def initiateLogin(self):
        self.login_button.clicked.connect(
            lambda: self.login_button_func(self.log_user_field.text(),
                                           self.log_pass_field.text())
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    LogRegWidget.login_button_func = lambda: print('arrrrrrrrrrrrrrrr')
    a = LogRegWidget()
    print(a.login_button_func)
    a.show()

    sys.exit(app.exec_())
