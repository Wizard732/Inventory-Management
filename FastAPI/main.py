from fastapi import FastAPI, Depends
from FastAPI.models import Data
from SQL.db import full_categories, categories
app = FastAPI()

@app.get("/categories")
def get_categories():
    return full_categories()

@app.post("/post_categories")
def post_category(item: Data):
    return categories(item)
