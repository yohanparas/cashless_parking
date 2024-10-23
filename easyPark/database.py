# database.py
import sqlite3
from user import User

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('parking_system.db') #connect to db
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY, password_hash TEXT, balance REAL)
        ''')
        self.conn.commit()

    def add_user(self, username, password_hash):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash, balance) VALUES (?, ?, ?)',
                       (username, password_hash, 0))
        self.conn.commit()

    def get_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        if user_data:
            user = User(user_data[0], user_data[1])
            user.balance = user_data[2]
            return user
        return None

    def update_balance(self, username, new_balance):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET balance = ? WHERE username = ?', (new_balance, username))
        self.conn.commit()
