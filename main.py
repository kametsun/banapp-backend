from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, Path
from DBHelper import execute_query
from repositories.Achievement import Achievement
from repositories.History import History, HistoryCreate
from repositories.Pet import PetCreate, HungerUpdate
from repositories.User import UserCreate, CoinUpdate, User

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


@app.get("/users/{user_id}/histories", response_model=List[History])
def get_user_histories(user_id: int):
    # SQLクエリを作成
    query = "SELECT * FROM banapp.histories WHERE user_id=%s"
    values = (user_id,)

    # クエリ実行
    results = execute_query(query, values, fetch=True)

    if not results:
        raise HTTPException(status_code=404, detail=f"No histories found for user with id {user_id}")

    return results


# -------------------- Pet --------------------
@app.post("/pets/", response_model=dict)
def create_pet(pet_data: PetCreate):
    query = "INSERT INTO banapp.pets (user_id, name, hunger) VALUES (%s, %s, %s)"
    values = (pet_data.user_id, pet_data.name, pet_data.hunger)
    return execute_query(query, values, fetch=False, return_id=True)


# 自分のペットのデータ
@app.get("/pets/{pet_id}")
def read_user(pet_id: int):
    query = "SELECT * FROM banapp.pets WHERE id=%s"
    values = (pet_id,)
    return execute_query(query, values, fetch=True)

@app.get("/pets/{pet_id}/death", response_model=dict)
def register_pet_death(pet_id: int):
    # 現在の時刻を取得
    death_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # SQLクエリを作成
    query = "UPDATE banapp.pets SET death_at = %s WHERE id=%s"
    values = (death_time, pet_id)

    # クエリを実行
    result = execute_query(query, values, fetch=False)

    # 結果の確認
    if result.get("message"):
        return {"death_time": death_time}
    else:
        raise HTTPException(status_code=404, detail=f"Pet with id {pet_id} not found")


# 空腹度変更
@app.patch("/pets/{pet_id}/hunger", response_model=dict)
def update_pet_hunger(hunger_data: HungerUpdate, pet_id: int = Path(..., description="The ID of the pet to update")):
    query = "UPDATE banapp.pets SET hunger = %s WHERE id=%s"
    values = (hunger_data.hunger, pet_id)
    result = execute_query(query, values, fetch=False)
    if result.get("message"):
        return {"message": f"Pet with id {pet_id} hunger updated successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Pet with id {pet_id} not found")


# -------------------- History --------------------

@app.post("/histories/")
def create_history(history: HistoryCreate):
    query = "INSERT INTO banapp.histories (user_id, pet_id, more_money) VALUES (%s, %s, %s)"
    values = (history.user_id, history.pet_id, history.more_money)
    return execute_query(query, values, fetch=False)

# -------------------- Achievement --------------------
@app.post("/achievements/")
def create_achievement(achievement: Achievement):
    query = "INSERT INTO banapp.get_achievements (user_id, achievement_id) VALUES (%s, %s)"
    values = (achievement.user_id, achievement.achievement_id)
    return execute_query(query, values, fetch=False)


# -------------------- Item --------------------
