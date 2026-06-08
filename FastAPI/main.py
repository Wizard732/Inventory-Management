from fastapi import FastAPI, Depends
from FastAPI.models import Data
from SQL.db import list_products, add_products, patch_in_products, \
    delete_by_id, return_categories, add_categories, filter_products_by_id, patch_products
app = FastAPI()

@app.get("/categories")
def get_categories():
    return return_categories()

@app.post("/post_categories")
def post_category(item: Data):
    return add_categories(item)

@app.get("/list_product")
def list_product():
    return list_products()

@app.get("/filter_product")
def filter(id: int):
    return filter_products_by_id(id)

@app.post("/add_product")
def add(item: Data):
    return add_products(item)

@app.patch("/patch_id")
def patch(id:int, quantity:int):
    return patch_products(id,quantity)

@app.delete("/delete")
def delete_id(id: int):
    return delete_by_id(id)