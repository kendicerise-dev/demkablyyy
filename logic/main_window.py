import sys
import os
import PySide6
from PySide6 import QtWidgets

from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from db_functions import fetch_products
from logic.product_card import ItemProduct

class MainWindow:
    def __init__(self, user_name = "Гость", role_name = "Гость"):
        # загрузка UI
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/main_window.ui")
        ui_file = QFile(ui_path)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # Подключение кнопок
        self.full_name_edit = self.window.findChild(QtWidgets.QLabel, "full_name_edit")
        self.full_name_edit.setText(user_name)
        self.exit_button = self.window.findChild(QtWidgets.QPushButton, "exit_button")
        self.exit_button.clicked.connect(self.exit_app)
        self.create_product_button = self.window.findChild(QtWidgets.QPushButton, "create_product_button")
        self.orders_button = self.window.findChild(QtWidgets.QPushButton, "orders_button")
        self.supplier_filter = self.window.findChild(QtWidgets.QComboBox, "supplier_filter")
        self.stock_filter = self.window.findChild(QtWidgets.QComboBox, "stock_filter")
        self.search_line = self.window.findChild(QtWidgets.QLineEdit, "search_line")
        self.logo = self.window.findChild(QtWidgets.QLabel, "label_4")

        self.stock_filter.currentIndexChanged.connect(self.apply_filters)
        self.supplier_filter.currentIndexChanged.connect(self.apply_filters)
        self.search_line.textChanged.connect(self.apply_filters)
        self.orders_button.clicked.connect(self.orders_app)

        logo_path = os.path.join(os.path.dirname(__file__), "../resources/Icon.png")

        self.logo.setPixmap(QPixmap(logo_path))

# Переменная для корректного оторажения функционала взависимости от роли
        self.role_name = role_name
        self.user_name = user_name

        if self.role_name in ["Гость", "Авторизованный пользователь"]:
            self.create_product_button.hide()
            self.orders_button.hide()
            self.supplier_filter.hide()
            self.stock_filter.hide()
            self.search_line.hide()

        if self.role_name == "Менеджер":
            self.create_product_button.hide()

        if self.role_name == "Администратор":
            pass

        # Настройка для отображения карточек товаров
        self.all_products = fetch_products()
        scroll_area = self.window.findChild(QtWidgets.QScrollArea, "scrollArea")
        scroll_content = scroll_area.widget()
        grid_layout = scroll_content.layout()
        self.product_layout: QtWidgets.QBoxLayout = grid_layout.itemAt(0).layout()
        self.supp_box()
        self.stock_box()
        self.apply_filters()
        #self.display_product(self.all_products)

    # Выход
    def exit_app(self):
        from .login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.window.show()
        self.window.close()

    # фильтрация
    def stock_box(self):
        self.stock_filter.addItem("Без сортировки")
        self.stock_filter.addItem("По возрастанию")
        self.stock_filter.addItem("По убыванию")

    def supp_box(self):
        self.supplier_filter.addItem("Все поставщики")
        suppliers = set(p["supplier"] for p in self.all_products)
        for s in sorted(suppliers):
            self.supplier_filter.addItem(s)

    def apply_filters(self):
        products = self.all_products
        # поиск
        text = self.search_line.text().lower()
        if text:
            products = [
                p for p in products
                if any(
                    text in str(value).lower()
                    for value in [
                        p["name"],
                        p["category"],
                        p["description"],
                        p["supplier"],
                        p["manufacturer"],
                        p["unit"]
                    ]
                )
            ]
        # фильтрация
        supplier = self.supplier_filter.currentText()
        if supplier != "Все поставщики":
            products = [p for p in products if p["supplier"] == supplier]
        #сортировка
        sort_type = self.stock_filter.currentText()
        if sort_type == "По возрастанию":
            products = sorted(products, key=lambda x: x["stock"])
        if sort_type == "По убыванию":
            products = sorted(products, key=lambda  x: x["stock"], reverse=True)
        # очистка
        for i in reversed(range(self.product_layout.count())):
            self.product_layout.itemAt(i).widget().setParent(None)

        self.display_product(products)

    # карточки товаров
    def display_product(self, products):
        for product in products:
            card = ItemProduct(product, self.role_name)
            self.product_layout.addWidget(card.ui)

    def orders_app(self):
        from logic.orders_window import OrdersWindow

        self.orders_window = OrdersWindow(
            self.role_name,
            self.user_name
        )

        self.orders_window.window.show()
        self.window.close()






