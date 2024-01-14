from pydantic import BaseModel


class User(BaseModel):
    name: str
    coin: int = 0
    cigarette_price: int


class CoinUpdate(BaseModel):
    coin: int
