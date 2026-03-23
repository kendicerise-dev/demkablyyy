import sys
import os
import PySide6


from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QApplication

from logic.login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Настройка стиля: фон, шрифт, текс, акцентные и дополнительные цвета
    app.setFont(QFont("Times New Roman", 12))
    app.setStyleSheet("""
    QWidget {
        background-color: #FFFFFF;
        font-family: "Times New Roman";
        color: black;
    }
    QPushButton {
        background-color: #00FA9A;
        color: black;
    }
    QPushButton:hover {
        background-color: #7FFF00;
    }
    """)

    # Настройка иконки приложения
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "Icon.png")
    app.setWindowIcon(QIcon(icon_path))
    # Открыть страницу авторизации
    login = LoginWindow()
    login.window.show()
    sys.exit(app.exec())


