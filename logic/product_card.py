import sys
import os
import PySide6
from PySide6 import QtWidgets

from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class ItemProduct:
    def __init__(self, product_data: dir, role_name = "Гость"):
        # загрузка UI
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/product_card.ui")
        ui_file = QFile(ui_path)

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.ui.category.setText(str(product_data.get("category")))
        self.ui.name.setText(str(product_data.get("name")))
        self.ui.description_edit.setText(str(product_data.get("description")))
        self.ui.manufacturer_edit.setText(str(product_data.get("manufacturer")))
        self.ui.supplier_edit.setText(str(product_data.get("supplier")))
        self.ui.price_edit.setText(str(product_data.get("new_price")))
        self.ui.unit_edit.setText(str(product_data.get("unit")))
        self.ui.stock_edit.setText(str(product_data.get("stock")))
        self.ui.discount_edit.setText(str(product_data.get("discount")))

        photo_name = str(product_data.get("photo"))
        photo_path = os.path.join(os.path.dirname(__file__), "../resources", photo_name)
        self.photo = self.ui.findChild(QtWidgets.QLabel, "photo")
        self.photo.setPixmap(QPixmap(photo_path))

        self.delete_button = self.ui.findChild(QtWidgets.QPushButton, "delete_button")

        if role_name != "Администратор":
            self.delete_button.hide()

        # Отображение карточек от скидок
        discount = int(product_data.get("discount") or 0)
        stock = int(product_data.get("stock") or 0)

        if stock == 0:
            self.ui.setStyleSheet("background-color:#87CEEB;")
        elif discount > 15:
            self.ui.setStyleSheet("background-color:#2E8B57;")


        old_price = float(product_data.get("old_price") or 0)
        new_price = float(product_data.get("new_price") or 0)
        self.product_data = product_data
        self.ui.mousePressEvent = self.open_edit

        # ---- отображение цены ----
        if discount > 0:
            # старая цена перечеркнута и красная
            self.ui.price_edit.setText(
                f"<span style='color:red; text-decoration:line-through'>{old_price}</span> "
                f"<span style='color:black'>{new_price}</span>"
            )
        else:
            self.ui.price_edit.setText(str(new_price))
        self.ui.setStyleSheet("")  # сброс фона
        # ---- подсветка фона ----
        if stock == 0:
            # голубой если товара нет
            self.ui.stock_edit.setStyleSheet("color:#87CEEB;")
        elif discount > 15:
            # зелёный если скидка >15%
            self.ui.setStyleSheet("background-color:#2E8B57;")


    def open_edit(self, event):
        if self.role_name != "Администратор":
            return

        if self.parent_window.edit_window_open:
            return

        from logic.product_form import ProductForm

        self.form = ProductForm(self.product_data, parent=self.parent_window)

        self.parent_window.edit_window_open = True
        self.form.window.show()
        self.form.window.destroyed.connect(self.parent_window.on_form_close)