import sqlite3
from pathlib import Path

DB_PATH = Path("data/memory.db")


def initialize_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_key TEXT UNIQUE NOT NULL,
                memory_value TEXT NOT NULL)"""
            )
        conn.commit()


def save_memory(key: str, value: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO memories (memory_key, memory_value)
            VALUES (?, ?)
            ON CONFLICT(memory_key)
            DO UPDATE SET memory_value = excluded.memory_value""", 
            (key, value))

        conn.commit()


def get_memory(key: str) -> str | None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT memory_value
            FROM memories
            WHERE memory_key = ?""", 
            (key,))

        row = cursor.fetchone()
        return row[0] if row else None
    
    
def get_all_memories() -> list[tuple[str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT memory_key, memory_value
            FROM memories
        """)
        return cursor.fetchall()


def search_memories(keywords: list[str]) -> list[tuple[str, str]]:
    if not keywords:
        return []

    conditions: list[str] = []
    parameters: list[str] = []

    for keyword in keywords:
        conditions.append("LOWER(memory_key) LIKE ?")
        parameters.append(f"%{keyword.lower()}%")

    where_clause = " OR ".join(conditions)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            f"""
            SELECT memory_key, memory_value
            FROM memories
            WHERE {where_clause}
            """,
            parameters
        )

        return cursor.fetchall()
    
    
def delete_memory(key: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            DELETE FROM memories
            WHERE memory_key = ?""", (key,))

        conn.commit()

        return cursor.rowcount > 0