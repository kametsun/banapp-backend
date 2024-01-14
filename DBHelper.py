from fastapi import HTTPException
from mysql.connector import Error

from repositories.InitDB import create_db_connection, close_db_connection


def execute_query(query: str):
    try:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection.is_connected():
            close_db_connection(connection)