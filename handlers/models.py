from pydantic import BaseModel, Field

class Data(BaseModel):
    id: int
    name: str = Field(max_length=20)
    price: int = Field(gt=5)
    stock_quantity: int = Field(gt=0)

