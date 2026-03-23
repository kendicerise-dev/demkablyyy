import sys
import os
import PySide6
from PySide6 import QtWidgets

from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class ItemOrder:
    def __init__(self, order_data: dir, role_name):
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/order_item.ui")
        ui_file = QFile(ui_path)

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.delete = self.ui.findChild(QtWidgets.QPushButton, "delete_2")
        if role_name != "Администратор":
            self.delete.hide()