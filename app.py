from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = '1110'

def get_db_connection():
    conn = sqlite3.connect(os.path.join('database', 'users.db'))
    conn.row_factory = sqlite3.Row
    return conn

def get_disciplina_db_connection():
    conn = sqlite3.connect(os.path.join('database', 'disciplinas.db'))
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
        faculdade = request.form['faculdade']
        curso = request.form['curso']
        periodo = request.form['periodo']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user:
            return render_template('forms.html', error="Usuário já cadastrado", name=name, email=email, faculdade=faculdade, curso=curso, periodo=periodo)
        if password != confirm_password:
            return render_template('forms.html', error="Senhas não coincidem", name=name, email=email, faculdade=faculdade, curso=curso, periodo=periodo)
        if not email.endswith('@ufrpe.br'):
            return render_template('forms.html', error="O e-mail deve ser do domínio @ufrpe.br", name=name, email=email, faculdade=faculdade, curso=curso, periodo=periodo)

        cursor.execute('INSERT INTO users (name, email, password, faculdade, curso, periodo) VALUES (?, ?, ?, ?, ?, ?)',
                       (name, email, password, faculdade, curso, periodo))
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
        session['user_id'] = user['id']
        if email == 'adm@ufrpe.br':
            return redirect(url_for('admin'))  
        return redirect(url_for('feed'))  
    else:
        return render_template('index.html', error="Conta não cadastrada")

    
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session['user_id']
    conn = get_disciplina_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form.get('disciplina_name')
        descricao = request.form.get('disciplina_desc')

        if nome:
            cursor.execute('INSERT INTO disciplinas (nome, descricao) VALUES (?, ?)', (nome, descricao))
            conn.commit()

    cursor.execute('SELECT * FROM disciplinas')
    disciplinas = cursor.fetchall()
    conn.close()

    return render_template('feed.html', user=user_id, disciplinas=disciplinas)

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
        return redirect(url_for('admin'))  

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('editar.html', user=user)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()

    if user['email'] != 'adm@ufrpe.br':
        conn.close()
        return redirect(url_for('feed'))

    if request.method == 'POST':
        if 'delete' in request.form:
            user_id_to_delete = request.form['delete']
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id_to_delete,))
            conn.commit()
    
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    return render_template('admin.html', users=users)

@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form['email']
    password = request.form['password']

    if email == 'adm@ufrpe.br' and password == 'adm':
        session['user_id'] = 1  
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('index', error="Credenciais inválidas"))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/disciplina')
def disciplina():
    return render_template('disciplina.html')

if __name__ == '__main__':
    app.run(debug=True)
