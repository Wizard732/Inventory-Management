from fastapi import FastAPI, Depends
from FastAPI.models import Data
from SQL.db import full_categories, categories, list_product, filter_products, add_products, patch_in_products, \
    delete_by_id, return_categories
app = FastAPI()

@app.get("/categories")
def get_categories():
    return return_categories()

@app.post("/post_categories")
def post_category(item: Data):
    return categories(item)

@app.get("/list_product")
def list_products():
    return list_product()

@app.get("/filter_product")
def filter(id: int):
    return filter_products(id)

@app.post("/add_product")
def add(item: Data):
    return add_products(item)

@app.patch("/patch_id")
def patch(id:int, quantity:int):
    return patch_in_products(id,quantity)

@app.delete("/delete")
def delete_id(id: int):
    return delete_by_id(id)