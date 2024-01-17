from pydantic import BaseModel


# JSONで渡す際のUserオブジェクト形式
class User(BaseModel):
    id: int
    name: str
    coin: int
    cigarette_price: int
    cigarette_per_day: int


class UserCreate(BaseModel):
    name: str
    coin: int = 0
    cigarette_price: int
    cigarette_per_day: int


class CoinUpdate(BaseModel):
    coin: int
