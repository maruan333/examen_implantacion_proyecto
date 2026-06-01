import os
import mysql.connector


def get_database_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "examuser"),
        password=os.getenv("DB_PASSWORD", "exam123"),
        database=os.getenv("DB_NAME", "examen"),
        autocommit=False,
    )
