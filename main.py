from fastapi import FastAPI, HTTPException, Path
from sqlalchemy.dialects.mssql import json

from DBHelper import execute_query
from repositories.Pet import PetCreate
from repositories.User import UserCreate, CoinUpdate

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# -------------------- User --------------------
# テーブル全件取得
@app.get("/{table_name}/")
def read_table_all(table_name: str):
    valid_table = ["users", "pets", "achievements", "items", "histories"]
    if table_name not in valid_table:
        raise HTTPException(status_code=404, detail="Table not found")
    return execute_query(f"SELECT * FROM banapp.{table_name}")


# users挿入
@app.post("/users/")
def create_users(user: UserCreate, response_model=int):
    query = "INSERT INTO banapp.users (name, coin, cigarette_price, cigarette_per_day) VALUES (%s, %s, %s, %s)"
    values = (user.name, user.coin, user.cigarette_price, user.cigarette_per_day)
    return execute_query(query, values, fetch=False, return_id=True)

@app.get("/users/{user_id}")
def read_user(user_id: int):
    query = "SELECT * FROM banapp.users WHERE id=%s"
    values = (user_id,)
    return execute_query(query, values, fetch=True)

# ユーザのコイン変更
@app.patch("/users/{user_id}/coin", response_model=dict)
def update_user_coin(coin_data: CoinUpdate, user_id: int = Path(..., description="The ID of the user to update")):
    query = "UPDATE banapp.users SET coin = %s WHERE id = %s"
    values = (coin_data.coin, user_id)
    result = execute_query(query, values, fetch=False)
    if result.get("message"):
        return {"message": f"User with id {user_id} coin updated successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


# -------------------- Pet --------------------
@app.post("/pets/", response_model=dict)
def create_pet(pet_data: PetCreate):
    query = "INSERT INTO banapp.pets (user_id, name, hunger) VALUES (%s, %s, %s)"
    values = (pet_data.user_id, pet_data.name, pet_data.hunger)
    return execute_query(query, values, fetch=False, return_id=True)
