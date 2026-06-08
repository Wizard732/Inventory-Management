
from SQL.config import HOST, USER, PASSWORD, DATABASE
from fastapi import HTTPException
import pymysql
from FastAPI.models import Data

from sqlalchemy import create_engine, Column, Integer, Float, String, select, DECIMAL
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(30))
    category_id = Column(Integer)
    quantity = Column(Integer, default=0)
    price = Column(DECIMAL(10,2))



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


def add_categories(item: Data):
    # add data in categories
    try:
        new_data = Categories(
        # add data with pydantic for sqlalchemy
            id = item.id,
            name = item.name
        )
        session.add(new_data)
        session.commit() # save data
        return(f"Данные успешно записаны в таблицу! {new_data.id}, {new_data.name}")

    except Exception as e:
        session.rollback() # if happened error
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении данных {e}.")


def list_products():
    # use a left join to connect table
    left_join = session.query(Products, Categories).outerjoin(Categories, Products.category_id == Categories.id)

    result = left_join.all() # result left join

    if not result:
        return("Таблицы пустые.")

    results = []
    for product, category in result : # product and category get item
        item_name = category.name if category else "Без категории" # if category exists use category.name if not on that category = Без категории
        results.append(f"{product.name} (Категория: {item_name})") # add data in results
    return(f"Список всех записей - {results}")



def filter_products_by_id(id: int):
    # if id == id return data
    try:
        result = select(Products).where(Products.id == id) # where query
        returns = session.execute(result).scalar_one_or_none() # Если строка есть, очисти её от лишних кортежей и дай мне сразу чистый объект продукта. Если строки нет, верни None

        if not returns:
            return("Такого id нет в базе")

        format_string = f"id - {returns.id} name - {returns.name}" # format the string for return
        return(f"Данные успешно отфильтрованы - {format_string}!")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при выполнении запроса: {e}.")



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

