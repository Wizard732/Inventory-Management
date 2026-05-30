from fastapi import FastAPI, Depends
from FastAPI.models import Data
from SQL.db import full_categories, categories,list_product
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
