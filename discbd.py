import sqlite3
import os

def get_db_connection():
    """Conecta ao banco de dados de disciplinas."""
    conn = sqlite3.connect(os.path.join('database', 'disciplinas.db'))  # Ajuste o caminho se necessário
    conn.row_factory = sqlite3.Row
    return conn

def visualizar_disciplinas():
    """Visualiza as disciplinas no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Buscar todas as disciplinas
    cursor.execute('SELECT * FROM disciplinas')
    disciplinas = cursor.fetchall()

    # Exibir as disciplinas
    if disciplinas:
        print("Disciplinas:")
        for disciplina in disciplinas:
            print(f"ID: {disciplina['id']}, Nome: {disciplina['nome']}, Descrição: {disciplina['descricao']}")
    else:
        print("Nenhuma disciplina encontrada.")

    conn.close()

if __name__ == "__main__":
    visualizar_disciplinas()
