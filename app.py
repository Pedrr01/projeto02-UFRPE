from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '1110'

import sqlite3
import os

def get_db_connection():
    conn = sqlite3.connect(os.path.join('database', 'users.db'))
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar se o e-mail já está cadastrado
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user:
            return render_template('forms.html', error="Usuário já cadastrado")
        if password != confirm_password:
            return render_template('forms.html', error="Senhas não coincidem")
        if not email.endswith('@ufrpe.br'):
            return render_template('forms.html', error="O e-mail deve ser do domínio @ufrpe.br")

        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                       (name, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))

    return render_template('forms.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']  # Armazenar o ID do usuário na sessão
        return redirect(url_for('feed'))
    else:
        return render_template('index.html', error="Conta não cadastrada")

@app.route('/feed')
def feed():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    return render_template('feed.html', user=user)

@app.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
def dashboard(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'edit' in request.form:
            return redirect(url_for('edit', user_id=user_id))
        elif 'delete' in request.form:
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('dashboard.html', user=user)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor.execute('UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?',
                       (name, email, password, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard', user_id=user_id))

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('editar.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
