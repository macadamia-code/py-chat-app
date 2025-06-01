import os
from dotenv import load_dotenv
import mysql.connector
import psycopg2

load_dotenv()

def get_connection():
    db_type = os.getenv("DB_TYPE")

    if db_type == "postgresql":
        # PostgreSQL用接続
        return psycopg2.connect(os.getenv("PGSQL_DATABASE_URL"))
    elif db_type == "mysql":
        # MySQL用接続
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )
    else:
        raise ValueError(f"Unsupported DB_TYPE: {db_type}")
