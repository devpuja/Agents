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


def search_memory(keyword: str, limit: int = 5):
    cursor.execute(
        """
        SELECT user_message, assistant_message
        FROM chat_history
        WHERE LOWER(user_message) LIKE LOWER(?)
        AND user_message NOT LIKE '%?'
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            f"%{keyword}%",
            limit
        )
    )

    return cursor.fetchall()
    

# print(search_memory("What is my name?"))
# print("\n\n+++++++++++++++++++++\n")
# print(search_memory("What database do I prefer?"))
# print("\n\n+++++++++++++++++++++\n")
# print(search_memory("What do I work on?"))

print(search_memory("name"))
print("\n\n+++++++++++++++++++++\n")
print(search_memory("my name"))
print("\n\n+++++++++++++++++++++\n")
print(search_memory("database"))
print("\n\n+++++++++++++++++++++\n")
print(search_memory("favorite"))
print("\n\n+++++++++++++++++++++\n")
print(search_memory("work"))