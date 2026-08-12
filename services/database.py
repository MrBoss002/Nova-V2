import sqlite3
import logging

DB_NAME = "nova_users.db"

def init_db():
    """Initializes SQLite database and creates users table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int, username: str = None, first_name: str = None) -> bool:
    """Adds a new user to database. Returns True if new user, False if existed."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone()
    
    is_new = False
    if not exists:
        cursor.execute(
            "INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        conn.commit()
        is_new = True
        
    conn.close()
    return is_new

def get_all_users() -> list:
    """Returns a list of all registered user IDs."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

def get_user_count() -> int:
    """Returns total number of registered users."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count
