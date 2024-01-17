from pydantic import BaseModel


class History(BaseModel):
    id: int
    user_id: int
    pet_id: int
    more_money: int


class HistoryCreate(BaseModel):
    user_id: int
    pet_id: int
    more_money: int
