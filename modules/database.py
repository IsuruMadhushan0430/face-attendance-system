import sqlite3
from pathlib import Path


DB_PATH = Path("database/attendance.db")


def create_database():
    DB_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_person(person_id, name):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO persons (person_id, name)
        VALUES (?, ?)
    """, (person_id, name))

    connection.commit()
    connection.close()


def get_person(person_id):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT person_id, name
        FROM persons
        WHERE person_id = ?
    """, (person_id,))

    result = cursor.fetchone()

    connection.close()

    return result