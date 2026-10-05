import sqlite3
from pathlib import Path
from datetime import datetime


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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            session_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(person_id, session_id)
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


def mark_attendance(
    person_id,
    name,
    session_id
):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    try:

        cursor.execute("""
            INSERT INTO attendance (
                person_id,
                name,
                date,
                time,
                session_id
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            person_id,
            name,
            date,
            time,
            session_id
        ))

        connection.commit()

        success = True

    except sqlite3.IntegrityError:

        success = False

    connection.close()

    return success


def get_attendance(session_id=None):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    if session_id:

        cursor.execute("""
            SELECT
                person_id,
                name,
                date,
                time
            FROM attendance
            WHERE session_id = ?
            ORDER BY time
        """, (session_id,))

    else:

        cursor.execute("""
            SELECT
                person_id,
                name,
                date,
                time
            FROM attendance
            ORDER BY date DESC, time DESC
        """)

    records = cursor.fetchall()

    connection.close()

    return records

def get_all_attendance():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            person_id,
            name,
            date,
            time,
            session_id
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records