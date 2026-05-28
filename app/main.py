from fastapi import FastAPI
from app.database import inventory_logic,stock_stats

app = FastAPI()

@app.get("/inventory")
def inventory():
    return inventory_logic()


@app.get("/api/v1/categories/stock-stats")
def stats():
    return stock_stats()