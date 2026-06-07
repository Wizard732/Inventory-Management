from SQL.config import HOST, USER, PASSWORD, DATABASE
from fastapi import HTTPException
import pymysql
from FastAPI.models import Data

from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

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


Base = declarative_base() # base for all table

class Categories(Base):
    # connect categories
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

# create engine
engine = create_engine(
    "mysql+pymysql://wizard:5732@localhost:3306/learn_sql"
)

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def return_categories():
    all_category = session.query(Categories).all()

    if len(all_category) == 0:
        return("Категория пустая.")

    result = []
    for category in all_category:
        result.append(f"Категория {category.name} успешно найдена!")
    return result




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


def filter_products(id:int):
    # sort product by id
    connection = connect()
    if not connection:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE id = %s" # maybe i'll add sort return
            cursor.execute(sql,(id,))

            row = cursor.fetchall()

            if not row:
                return {"error": "ID отсутствует в базе данных"}
        return {"message": f"Сортировка завершена успешно {row}!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД {e}")
    finally:
        if connection:
            connection.close()


def add_products(item: Data):
    # add data in products
    connection = connect()
    if not connection:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД")

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO products (id,name,category_id, quantity, price) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql,(item.id,item.name,item.category_id,item.quantity,item.price))
            connection.commit()

        return {"message": "Данные успешно добавлены!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД {e}")
    finally:
        if connection:
            connection.close()


def patch_in_products(id: int, quantity: int):
    # patch product
    connection = connect()
    if not connection:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД")

    try:
        with connection.cursor() as cursor:
            sql = "UPDATE products SET quantity = %s WHERE id = %s" # update quantity on (int quantity) if id = id
            cursor.execute(sql,(quantity,id))

            connection.commit()

            if cursor.rowcount == 0:
                return {"error": "Товар не найден или количество уже совпадает."}
        return {"message": f"Количество успешно изменено на {quantity}!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД {e}")
    finally:
        if connection:
            connection.close()


def delete_by_id(id:int):
    # delete data by id
    connection = connect()
    if not connection:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД")

    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products WHERE id = %s"
            cursor.execute(sql,(id,))

            connection.commit()

        return {"message": "Данные успешно удалены!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось подключиться к БД {e}")
    finally:
        if connection:
            connection.close()

