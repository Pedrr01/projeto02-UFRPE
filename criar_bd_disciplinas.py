import sqlite3
import os

def create_database():
    # Caminho do banco de dados
    database_path = os.path.join('database', 'disciplinas.db')
    
    # Conexão com o banco de dados
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    # Criação da tabela disciplinas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    
    # Commit e fechamento da conexão
    conn.commit()
    conn.close()
    print('Banco de dados de disciplinas criado com sucesso.')

if __name__ == '__main__':
    create_database()
