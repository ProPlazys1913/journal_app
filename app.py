from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def connect_db():
    return sqlite3.connect('database.db')

def init_db():
    with connect_db() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        ''')
init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        with connect_db() as db:
            try:
                db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                db.commit()
            except sqlite3.IntegrityError:
                flash('Username already exists.')
                return redirect(url_for('register'))
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with connect_db() as db:
            user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    with connect_db() as db:
        entries = db.execute('SELECT * FROM entries WHERE user_id = ? ORDER BY timestamp DESC', (session['user_id'],)).fetchall()
    return render_template('dashboard.html', entries=entries)

@app.route('/entry', methods=['GET', 'POST'])
@login_required
def entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        with connect_db() as db:
            db.execute('INSERT INTO entries (user_id, title, content) VALUES (?, ?, ?)', (session['user_id'], title, content))
            db.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('entry.html')

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    with connect_db() as db:
        entry = db.execute('SELECT * FROM entries WHERE id = ? AND user_id = ?', (entry_id, session['user_id'])).fetchone()
        
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            
            db.execute('UPDATE entries SET title = ?, content = ? WHERE id = ? AND user_id = ?', (title, content, entry_id, session['user_id']))
            db.commit()
            return redirect(url_for('dashboard'))
    
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    with connect_db() as db:
        db.execute('DELETE FROM entries WHERE id = ? AND user_id = ?', (entry_id, session['user_id']))
        db.commit()
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
