import bcrypt
import sqlite3
from WCSUGaming import app, g
from contextlib import closing

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def validate_user(username, password):
    req = g.db.execute('SELECT username, password, privilege \
                        FROM users WHERE username=?', [username])
    user = req.fetchone()
    print(user)
    if user and bcrypt.hashpw(password, user[1]) == user[1]:
        return (user[0], user[2])
    else:
        return None

def register_user(username, password, email):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        g.db.execute('INSERT INTO users \
                     (username, password, email, privilege) \
                     VALUES (?, ?, ?, ?)', [username, hashed, email, 0])
        g.db.commit()
        return None
    except sqlite3.Error as e:
        return "An error occurred: " + e.args[0]