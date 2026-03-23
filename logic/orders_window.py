import sys
import os
import PySide6
from PySide6 import QtWidgets

from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from db_functions import get_orders
from logic.order_card import ItemOrder

class OrdersWindow:
    def __init__(self, role_name, user_name):
        self.role_name = role_name
        self.user_name = user_name

        ui_path = os.path.join(os.path.dirname(__file__), "../ui/orders_window.ui")
        ui_file = QFile(ui_path)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.add_otder = self.window.findChild(QtWidgets.QPushButton, "add_otder")
        self.cancel = self.window.findChild(QtWidgets.QPushButton, "cancel")
        self.cancel.clicked.connect(self.cancel_window)

        if role_name == "Менеджер":
            self.add_otder.hide()

        self.all_orders = get_orders()
        scroll_area = self.window.findChild(QtWidgets.QScrollArea, "scrollArea")
        scroll_content = scroll_area.widget()
        grid_layout = scroll_content.layout()
        self.orders_items: QtWidgets.QBoxLayout = grid_layout.itemAt(0).layout()

        self.display_orders(self.all_orders)

    def cancel_window(self):
        from logic.main_window import MainWindow

        self.main_window = MainWindow(
            user_name=self.user_name,
            role_name=self.role_name
        )

        self.main_window.window.show()
        self.window.close()



    def display_orders(self, orders):
        for order in orders:
            card = ItemOrder(order, self.role_name)
            self.orders_items.addWidget(card.ui)



