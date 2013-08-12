import bcrypt
import sqlite3
from WCSUGaming import app, g

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def validate_user(username, password):
    req = g.db.execute('SELECT username, password, privilege
                        FROM users WHERE username=?', [username])
    user = req.fetchall()
    if bcrypt.hashpw(password, user[1]) == user[1]:
        return (username, privilege)
    else:
        return None

def register_user(username, password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        g.db.execute('INSERT INTO users (username, password, privilege)
                      VALUES (?, ?, ?)', [username, hashed, 0])
        g.db.commit()
    except sqlite3.Error as e:
        print("An error occurred: ", e.args[0])