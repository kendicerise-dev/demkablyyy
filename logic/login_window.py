import sys
import os
import PySide6
from PySide6 import QtWidgets

from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from logic.main_window import MainWindow
from db_functions import get_user

class LoginWindow:
    def __init__(self):
        # загрузка UI
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/login_window.ui")
        ui_file = QFile(ui_path)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # Подключение кнопок
        self.login_button = self.window.findChild(QtWidgets.QPushButton, "login_button")
        self.guest_button = self.window.findChild(QtWidgets.QPushButton, "guest_button")
        self.window.login_button.clicked.connect(self.login)
        self.window.guest_button.clicked.connect(self.login_as_guest)
        self.logo = self.window.findChild(QtWidgets.QLabel, "label")

        logo_path = os.path.join(os.path.dirname(__file__), "../resources/Icon.png")

        self.logo.setPixmap(QPixmap(logo_path))


# Войти как гость
    def login_as_guest(self):
        self.main_window = MainWindow(
            user_name="Гость",
            role_name = "Гость"
        )
        self.main_window.window.show()
        self.window.close()

    def login(self):
        login = self.window.line_login.text().strip()
        password = self.window.line_password.text().strip()

        if not login or not password:
            QMessageBox.warning(
                self.window,
                "Ошибка",
                "Введите логин и пароль"
            )
            return

        user = get_user(login, password)
        if user is None:
            QMessageBox.warning(
                self.window,
                "Ошибка",
                "Неверный логин или пароль"
            )
            return

        self.main_window = MainWindow(
            user_name=user["user_name"],
            role_name = user["role_name"]
        )
        self.main_window.window.show()
        self.window.close()


