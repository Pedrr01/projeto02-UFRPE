import sqlite3
import os

db_path = os.path.join('database', 'users.db')

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

connection.commit()
connection.close()
