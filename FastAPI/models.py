from pydantic import BaseModel, Field

class Data(BaseModel):
    id: int
    name: str = Field(not None, max_length=30)
    category_id: int
    quantity: int = Field(default=0)
    price: float = Field(le=50000)