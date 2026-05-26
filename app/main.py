from fastapi import FastAPI
from app.database import inventory_logic

app = FastAPI()

@app.get("/inventory")
def inventory():
    return inventory_logic()