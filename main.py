from fastapi import FastAPI, HTTPException
from DBHelper import execute_query

app = FastAPI()

@app.get("/{table_name}/")
def read_table_all(table_name: str):
    valid_table = ["users", "pets", "achievements", "items", "histories"]
    if table_name not in valid_table:
        raise HTTPException(status_code=404, detail="Table not found")
    return execute_query(f"SELECT * FROM banapp.{table_name}")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
