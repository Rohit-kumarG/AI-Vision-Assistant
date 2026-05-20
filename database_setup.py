import sqlite3
import os

# Database file banao
db_path = "database/users.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Users table banao
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        visits      INTEGER DEFAULT 1,
        last_emotion TEXT,
        last_seen   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("✅ Database ready!")