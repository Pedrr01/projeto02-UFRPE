import sqlite3
import os

db_path = os.path.join('database', 'users.db')

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Password: {row[3]}")

connection.close()
