from sys import exception

import psycopg2
from config import DB_CONFIG

def fetch_products():
    conn = psycopg2.connect(**DB_CONFIG)
    products = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
    select 
        p.product_name,
        p.product_description,
        p.product_price,
        p.product_discount,
        p.product_photo,
        p.product_stock_quantity,
        c.category_name,
        s.supplier_name,
        m.manufacturer_name,
        u.unit_name
    from products p
    left join categories c on c.category_id = p.category_id
    left join suppliers s on s.supplier_id = p.supplier_id
    left join manufacturers m on m.manufacturer_id = p.manufacturer_id
    left join units u on u.unit_id = p.unit_id
    """)
        for row in cursor.fetchall():
            (name,description,price,discount,photo,stock, category, supplier,manufacturer,unit) = row
            price = float(price or 0)
            discount = int(discount or 0)
            old_price = round(price/(1 - discount/100), 2) if discount else price

            products.append({
                "name": name,
                "description": description,
                "new_price": price,
                "old_price": old_price,
                "discount": discount,
                "photo": photo,
                "stock": stock,
                "category": category,
                "supplier": supplier,
                "manufacturer": manufacturer,
                "unit": unit
            })
        return products
    except Exception as e:
        print("products", e)
        return None
    finally:
        conn.close()

def get_user(login, password):
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        cursor = conn.cursor()
        cursor.execute("""
        select 
            u.user_full_name,
            r.role_name
           
        from users u 
        join roles r on r.role_id = u.role_id
        where u.user_login = %s and u.user_password =%s
        """, (login, password))
        row = cursor.fetchone()
        if row:
            user = {"user_name": row[0], "role_name": row[1]}
            return user
        else:
            return None
    except Exception as e:
        print("user", e)
        return None
    finally:
        conn.close()

def get_orders():
    conn = psycopg2.connect(**DB_CONFIG)
    orders = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
        select
            p.product_article,
            s.status_name,
            pp.pickup_point_name,
            o.order_date,
            o.order_delivary_date, 
            oi.product_quantity,
            u.user_full_name
        from orders o
        left join order_items oi on oi.order_id = o.order_id
        left join products p on p.product_id = oi.product_id
        left join users u on u.user_id = o.user_id
        left join pickup_points pp on pp.pickup_point_id = o.pickup_point_id
        left join statuses s on s.status_id = o.status_id
        """)
        for row in cursor.fetchall():
            (article, status, pickup_point, date,delivary_date, stock, user_name) = row

            orders.append({
                "article": article,
                "status": status,
                "pickup_point": pickup_point,
                "date": date,
                "delivary_date": delivary_date,
                "stock": stock,
                "user_name":user_name
            })
        return orders
    except Exception as e:
        print("orders", e)
        return None
    finally:
        conn.close()
def save_product(self):
    import psycopg2
    from config import DB_CONFIG

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
                product_price,
                product_discount,
                product_stock_quantity,
                supplier_id,
                manufacturer_id,
                unit_id,
                category_id,
                product_description
            )
            VALUES (%s,%s,%s,%s,%s,1,1,1,1,'-')
            """, (article, name, price, discount, stock))

        conn.commit()
        self.window.close()

    except Exception as e:
        print("Ошибка:", e)
    finally:
        conn.close()


