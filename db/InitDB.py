import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


# MySQL接続関数
def create_db_connection():
    try:
        load_dotenv()
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("MySQL DB connection successful")
        return connection
    except Error as erorr:
        print(f"Error while connecting to MySQL {erorr}")


# データベースとの接続を切る
def close_db_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL DB connection is closed")


# データベース作成
def create_database():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"{db_name} Database created successfully")
    except Error as error:
        print(f"Failed to create database {db_name} {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)


def drop_database():
    load_dotenv()
    db_name: str = os.getenv("DB_NAME")
    try:
        connection = create_db_connection()
        if connection is not None:
            cursor = connection.cursor()

            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            print(f"{db_name} Database dropped successfully")
    except Error as error:
        print(f"Failed to drop database {db_name} {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            close_db_connection(connection)


drop_database()
create_database()

