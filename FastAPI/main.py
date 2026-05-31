from fastapi import FastAPI, Depends
from FastAPI.models import Data
from SQL.db import full_categories, categories,list_product, filter_products
app = FastAPI()

@app.get("/categories")
def get_categories():
    return full_categories()

@app.post("/post_categories")
def post_category(item: Data):
    return categories(item)

@app.get("/list_product")
def list_products():
    return list_product()

@app.get("/filter_product")
def filter(id: int):
    return filter_products(id)