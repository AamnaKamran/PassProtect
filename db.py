import sqlite3

# === Classes ===

class User:
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

class Credential:
    def __init__(self, app_name, user_name, email, password):
        self.app_name = app_name
        self.user_name = user_name
        self.email = email
        self.password = password

# === Database Setup ===

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_name TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_name TEXT NOT NULL,
        user_name TEXT NOT NULL,
        email TEXT,
        password TEXT NOT NULL,
        user_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_name)
    )
    ''')

    conn.commit()

# === Insert Functions ===

def insert_user(user):
    cursor.execute('INSERT INTO users (user_name, password) VALUES (?, ?)', (user.user_name, user.password))
    conn.commit()
    return cursor.lastrowid

def insert_credential(credential, user_id):
    cursor.execute('''
        INSERT INTO credentials (app_name, user_name, email, password, user_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (credential.app_name, credential.user_name, credential.email, credential.password, user_id))
    conn.commit()

def user_exists(username):
    cursor.execute('SELECT * FROM users WHERE user_name = ?', (username,))
    return cursor.fetchone()

def fetch_credentials_for_user(user_id):
    cursor.execute('''
        SELECT app_name, user_name, email, password
        FROM credentials
        WHERE user_id = ?
    ''', (user_id,))
    return cursor.fetchall()
