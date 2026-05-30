from SQL.config import HOST, USER, PASSWORD, DATABASE
from fastapi import HTTPException
import pymysql
from FastAPI.models import Data



def connect():
    try:
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД {e}")


def full_categories():
    connection = connect() # connect to sql
    if not connection:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM categories" # return all name in categories
            cursor.execute(sql)

            row = cursor.fetchall()
        return {"message": f"Список всех категорий - {row}!"}

    except Exception as e: # if exception
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД {e}")
    finally:
        if connection:
            connection.close()


def categories(item: Data):
    connection = connect()
    if not connection:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД")

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO categories (id,name) VALUES (%s, %s)"  # push data in sql
            cursor.execute(sql,(item.id, item.name))
            connection.commit()

        return {"message": "Новая категория успешно создана!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД {e}")
    finally:
        if connection:
            connection.close()


def list_product():
    # return list full product
    connection = connect()
    if not connection:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT products.name FROM products LEFT JOIN categories ON products.category_id = categories.id"
            cursor.execute(sql)

            row = cursor.fetchall()
        return {"message": f"Список всех товаров - {row}!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД {e}")
    finally:
        if connection:
            connection.close()