import sqlite3
import os

# Caminho para o banco de dados
db_path = os.path.join('database', 'users.db')

# Conexão com o banco de dados
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Criar tabela 'users' se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Verificar as colunas existentes na tabela 'users'
cursor.execute("PRAGMA table_info(users)")
columns = [column[1] for column in cursor.fetchall()]

# Adicionar a coluna 'faculdade' se ela não existir
if 'faculdade' not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN faculdade TEXT")
    print("Coluna 'faculdade' adicionada com sucesso.")

# Adicionar a coluna 'curso' se ela não existir
if 'curso' not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN curso TEXT")
    print("Coluna 'curso' adicionada com sucesso.")

# Adicionar a coluna 'periodo' se ela não existir
if 'periodo' not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN periodo TEXT")
    print("Coluna 'periodo' adicionada com sucesso.")

# Confirma as alterações e fecha a conexão
connection.commit()
connection.close()
