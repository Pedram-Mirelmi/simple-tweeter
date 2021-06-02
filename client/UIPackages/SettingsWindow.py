from typing import Union

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
# from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLineEdit, QMainWindow
from client.BackendPackages.RH_client import RequestHandler
from client.BackendPackages.ClientKeywords import *
from client.UIPackages.PopupWindow import popBox
import re
from datetime import datetime


def isEmail(email_address: str):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return bool(re.match(pattern, email_address))


class SettingsWindowUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(432, 494)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.setFields()
        self.addSpacers()
        self.setButtons()
        self.addWidgetsToLayout()
        self.initiateTexts()

    def setFields(self):
        self.username_label = QtWidgets.QLabel(self.central_widget)
        self.username_field = QtWidgets.QLineEdit(self.central_widget)
        # self.username_field.setFixedSize(306, 25)
        self.name_label = QtWidgets.QLabel(self.central_widget)
        self.name_field = QtWidgets.QLineEdit(self.central_widget)
        # self.name_field.setFixedSize(306, 25)
        self.password_label = QtWidgets.QLabel(self.central_widget)
        self.password_field = QtWidgets.QLineEdit(self.central_widget)
        # self.password_field.setFixedSize(306, 25)
        self.email_label = QtWidgets.QLabel(self.central_widget)
        self.email_field = QtWidgets.QLineEdit(self.central_widget)
        # self.email_field.setFixedSize(306, 25)
        self.phone_label = QtWidgets.QLabel(self.central_widget)
        self.phone_field = QtWidgets.QLineEdit(self.central_widget)
        # self.phone_field.setFixedSize(170, 25)
        self.gender_label = QtWidgets.QLabel(self.central_widget)
        self.male_button = QtWidgets.QRadioButton(self.central_widget)
        self.male_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.female_button = QtWidgets.QRadioButton(self.central_widget)
        self.female_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.birthday_label = QtWidgets.QLabel(self.central_widget)
        self.birthday_field = QtWidgets.QDateEdit(self.central_widget)
        self.birthday_field.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.birthday_field.setDisplayFormat("yyyy-M-dd")
        self.bio_label = QtWidgets.QLabel(self.central_widget)
        self.bio_field = QtWidgets.QTextEdit(self.central_widget)

    def setButtons(self):
        self.save_button = QtWidgets.QPushButton(self.central_widget)
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        save_icon = QtGui.QIcon()
        save_icon.addPixmap(QtGui.QPixmap("../../../../../Pictures/checkIc.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_button.setIcon(save_icon)

    def addSpacers(self):
        spacer_item = QtWidgets.QSpacerItem(131, 26, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacer_item1 = QtWidgets.QSpacerItem(131, 26, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacer_item2 = QtWidgets.QSpacerItem(185, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacer_item3 = QtWidgets.QSpacerItem(357, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacer_item4 = QtWidgets.QSpacerItem(217, 22, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacer_item, 4, 5, 1, 2)
        self.gridLayout.addItem(spacer_item1, 5, 5, 1, 2)
        self.gridLayout.addItem(spacer_item2, 6, 4, 1, 3)
        self.gridLayout.addItem(spacer_item3, 7, 1, 1, 6)
        self.gridLayout.addItem(spacer_item4, 9, 0, 1, 4)

    def addWidgetsToLayout(self):
        self.gridLayout.addWidget(self.username_label, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.username_field, 0, 2, 1, 5)
        self.gridLayout.addWidget(self.name_label, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.name_field, 1, 2, 1, 5)
        self.gridLayout.addWidget(self.password_label, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.password_field, 2, 2, 1, 5)
        self.gridLayout.addWidget(self.email_label, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.email_field, 3, 2, 1, 5)
        self.gridLayout.addWidget(self.phone_label, 4, 0, 1, 2)
        self.gridLayout.addWidget(self.phone_field, 4, 2, 1, 3)
        self.gridLayout.addWidget(self.gender_label, 5, 0, 1, 2)
        self.gridLayout.addWidget(self.male_button, 5, 2, 1, 1)
        self.gridLayout.addWidget(self.female_button, 5, 3, 1, 2)
        self.gridLayout.addWidget(self.birthday_label, 6, 0, 1, 2)
        self.gridLayout.addWidget(self.birthday_field, 6, 2, 1, 2)
        self.gridLayout.addWidget(self.bio_label, 7, 0, 1, 1)
        self.gridLayout.addWidget(self.bio_field, 8, 0, 1, 7)
        self.gridLayout.addWidget(self.save_button, 9, 0, 1, 2)

    def initiateTexts(self):
        self.setWindowTitle("self")
        self.username_label.setText("Username")
        self.name_label.setText("Name")
        self.password_label.setText("Password")
        self.email_label.setText("Email")
        self.phone_label.setText("Phone.Num")
        self.gender_label.setText("gender")
        self.male_button.setText("Male")
        self.female_button.setText("Female")
        self.birthday_label.setText("birthday")
        self.bio_label.setText("Bio")
        self.save_button.setText(" Save")


class SettingsWindow(SettingsWindowUI):
    def __init__(self, req_handler: RequestHandler, user_info: dict[str, str]):
        super().__init__()
        self.user_info = user_info
        self.req_handler = req_handler
        self.save_button.clicked.connect(
            self.saveButtonClicked
        )

    def saveButtonClicked(self):
        if isEmail(self.email_field.text()) or not self.email_field.text().strip():
            response = self.req_handler.updateProfile(self.getNewProfileInfo())
            if response[OUTCOME]:
                popBox(SUCCESS, "Your Changes successfully saved!",
                       QtWidgets.QMessageBox.Information, [QtWidgets.QMessageBox.Ok])
                self.user_info.update(self.getNewProfileInfo())
            else:
                popBox(FAILED, response[STATUS], QtWidgets.QMessageBox.Critical,
                       [QtWidgets.QMessageBox.Ok])
        else:
            popBox(FAILED, "Invalid email address", QtWidgets.QMessageBox.Critical,
                   [QtWidgets.QMessageBox.Ok])

    def getNewProfileInfo(self):
        return {
            USERNAME: self.getProperString(self.username_field.text()),
            NAME: self.getProperString(self.name_field.text()),
            PASSWORD: self.getProperString(self.password_field.text()),
            EMAIL: self.getProperString(self.email_field.text()),
            PHONE: self.getProperString(self.phone_field.text()),
            GENDER: self.getGender(),
            BIRTHDAY: '-'.join(list(map(str, self.birthday_field.date().getDate()))),
            BIO: self.getProperString(self.bio_field.toPlainText())
        }

    def initiateFields(self, user_info: dict[str, str]):
        self.username_field.setText(user_info.get(USERNAME, ''))
        self.name_field.setText(user_info.get(NAME, ''))
        self.password_field.setText(user_info.get(PASSWORD, ''))
        self.email_field.setText(user_info.get(EMAIL, ''))
        self.phone_field.setText(user_info.get(PHONE, ''))
        if user_info[GENDER] == 'M':
            self.male_button.setChecked(True)
        elif user_info[GENDER] == 'F':
            self.female_button.setChecked(True)
        if user_info[BIRTHDAY]:
            self.birthday_field.setDate(QDate(*map(int, user_info.get(BIRTHDAY, '0001-01-01').split('-'))))
        self.bio_field.setText(user_info.get(BIO, ''))

    @staticmethod
    def getProperString(s: str) -> Union[None, str]:
        if not s:
            return None
        return s

    def getGender(self) -> Union[None, str]:
        if self.male_button.isChecked():
            return 'M'
        if self.female_button.isChecked():
            return 'F'
        return None


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    t = SettingsWindow(None, {BIRTHDAY: '2000-12-25'})
    t.show()
    sys.exit(app.exec_())

    # print(isEmail("mirelmipedram@gmail.com"))
