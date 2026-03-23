import os
import psycopg2
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from config import DB_CONFIG


class ProductForm:
    def __init__(self, product=None, parent=None):
        self.product = product
        self.parent = parent

        ui_path = os.path.join(os.path.dirname(__file__), "../ui/change_product_window.ui")
        ui_file = QFile(ui_path)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # поля
        self.article = self.window.findChild(QtWidgets.QLineEdit, "article")
        self.name = self.window.findChild(QtWidgets.QLineEdit, "name")
        self.price = self.window.findChild(QtWidgets.QLineEdit, "price")
        self.discount = self.window.findChild(QtWidgets.QLineEdit, "discount")
        self.stock = self.window.findChild(QtWidgets.QLineEdit, "stock")

        self.save_btn = self.window.findChild(QtWidgets.QPushButton, "change")
        self.cancel_btn = self.window.findChild(QtWidgets.QPushButton, "cancel")

        self.cancel_btn.clicked.connect(self.window.close)
        self.save_btn.clicked.connect(self.save_product)

        # режим редактирования
        if self.product:
            self.fill_data()

    def fill_data(self):
        self.article.setText(str(self.product.get("article", "")))
        self.name.setText(str(self.product.get("name", "")))
        self.price.setText(str(self.product.get("new_price", "")))
        self.discount.setText(str(self.product.get("discount", "")))
        self.stock.setText(str(self.product.get("stock", "")))

    def save_product(self):
        conn = psycopg2.connect(**DB_CONFIG)
        try:
            cursor = conn.cursor()

            article = self.article.text()
            name = self.name.text()
            price = float(self.price.text() or 0)
            discount = int(self.discount.text() or 0)
            stock = int(self.stock.text() or 0)

            if self.product:  # UPDATE
                cursor.execute("""
                UPDATE products
                SET product_name=%s,
                    product_price=%s,
                    product_discount=%s,
                    product_stock_quantity=%s
                WHERE product_article=%s
                """, (name, price, discount, stock, article))

            else:  # INSERT
                cursor.execute("""
                INSERT INTO products (
                    product_article,
                    product_name,
                    product_description,
                    product_price,
                    product_discount,
                    product_stock_quantity,
                    supplier_id,
                    manufacturer_id,
                    unit_id,
                    category_id
                )
                VALUES (%s,%s,'-',%s,%s,%s,1,1,1,1)
                """, (article, name, price, discount, stock))

            conn.commit()
            self.window.close()

        except Exception as e:
            print("Ошибка:", e)
        finally:
            conn.close()