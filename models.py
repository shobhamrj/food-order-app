from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: str | None = None
    password: str


class FoodItem(BaseModel):
    name: str
    quantity: int
    unit_price: float


class Order(BaseModel):
    user_id: int | None = None
    food_items: list[FoodItem]
    total_price: float
