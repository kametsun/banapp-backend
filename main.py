from fastapi import FastAPI, HTTPException, Path
from DBHelper import execute_query
from repositories.User import User, CoinUpdate

app = FastAPI()


# テーブル全件取得
@app.get("/{table_name}/")
def read_table_all(table_name: str):
    valid_table = ["users", "pets", "achievements", "items", "histories"]
    if table_name not in valid_table:
        raise HTTPException(status_code=404, detail="Table not found")
    return execute_query(f"SELECT * FROM banapp.{table_name}")


# users挿入
@app.post("/users/")
def create_users(user: User, response_model=int):
    query = "INSERT INTO banapp.users (name, coin, cigarette_price) VALUES (%s, %s, %s)"
    values = (user.name, user.coin, user.cigarette_price)
    return execute_query(query, values, fetch=False, return_id=True)

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

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
