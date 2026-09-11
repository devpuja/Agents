import sqlite3

conn = sqlite3.connect(
    "data/memory.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(
    id INTEGER PRIMARY KEY,
    user_message TEXT,
    assistant_message TEXT
)
""")

conn.commit()


def save_chat(user: str, assistant: str):
    cursor.execute(
        """
        INSERT INTO chat_history
        (user_message,assistant_message)
        VALUES (?,?)
        """,
        (user, assistant)
    )
    conn.commit()


def get_history():
    cursor.execute(
        """
        SELECT user_message,
        assistant_message
        FROM chat_history
        ORDER BY id DESC
        LIMIT 10
        """
    )
    return cursor.fetchall()

def search_memory(keyword: str):
    cursor.execute(
        """
        SELECT user_message,
               assistant_message
        FROM chat_history
        WHERE user_message LIKE ?
        ORDER BY id DESC
        LIMIT 5
        """,
        (f"%{keyword}%",)
    )
    return cursor.fetchall()
    