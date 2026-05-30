from fastapi import FastAPI, Depends
from FastAPI.models import Data
from SQL.db import full_categories
app = FastAPI()

@app.get("/categories")
def categories():
    return full_categories()


