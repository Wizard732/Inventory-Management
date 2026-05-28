import pymysql
from app.config import HOST, DATABASE, USERNAME, PASSWORD
from fastapi import Depends
from handlers.models import Data




def get_connect():
    try:
        connection = pymysql.connect(
            host= HOST,
            database=DATABASE, # connect to sql in pymysql
            user=USERNAME,
            password=PASSWORD
        )
        return connection
    except Exception as e:
        return {"error": f"Ошибка подключения к БД {e}"}


def inventory_logic():
    # JOIN TABLE AND CHECK DATA
    connection = get_connect()
    if not connection:
        return {"error": "Не удалось подключится к БД"}

    try:
        with connection.cursor() as cursor:
            sql = "SELECT warehouses.address, SUM(products.price * products.stock_quantity) AS total_price_product FROM warehouses JOIN products ON products.warehouse_id = warehouses.id GROUP BY warehouses.address ORDER BY total_price_product DESC"
            cursor.execute(sql)

            row = cursor.fetchall()
            return {"message": f"Данные успешно проверенны {row}."}

    except Exception as e:
        return {"error": f"Ошибка подключения к БД {e}"}
    finally:
        if connection:
            connection.close()


def stock_stats():
    connection = get_connect()
    if not connection:
        return {"error": "Не удалось подключится к БД"}

    try:
        with connection.cursor() as cursor:
            # left join
            sql = "SELECT categories.name, COALESCE(SUM(products.quantity),0) AS big_quantity FROM categories LEFT JOIN products ON categories.id = products.category_id GROUP BY categories.name ORDER BY big_quantity DESC"
            cursor.execute(sql)

            row = cursor.fetchall() # post sql data
            return {"message":f"Список категорий успешно отправлен {row}!"}

    except Exception as e: # if return exception
        return {"error": f"Ошибка при отправлении списка категорий {e}"}
    finally:
        if connection:
            connection.close()