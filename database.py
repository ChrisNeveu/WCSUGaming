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

# String, String -> (Bool, Either Int Error)
def validate_user(username, password):
    try:
        req = g.db.execute('SELECT username, password, privilege \
                            FROM users WHERE username=?', [username])
        user = req.fetchone()
        if user and bcrypt.hashpw(password, user[1]) == user[1]:
            return (True, user[2])
        else:
            return (False, "Incorrect Password")
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String, String, String -> (Bool, Maybe Error)
def register_user(username, password, email):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        g.db.execute('INSERT INTO users \
                      (username, password, email, privilege) \
                      VALUES (?, ?, ?, ?)', [username, hashed, email, 0])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String, String, String, String -> (Bool, Maybe Error)
def update_user(username, password, email, privilege):
    try:
        if password is None:
            g.db.execute('UPDATE users SET email=?, privilege=? \
                          WHERE username=?',
                         [email, privilege, username])
        else:
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            g.db.execute('UPDATE users SET password=?, \
                          email=?, privilege=? \
                          WHERE username=?',
                         [hashed, email, privilege, username])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Maybe Error)
def delete_user(username):
    try:
        g.db.execute('DELETE FROM users WHERE username=?',
                     [username])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Either Int Error)
def get_user(username):
    try:
        req = g.db.execute('SELECT username, email, privilege \
                            FROM users WHERE username=?', [username])
        user = req.fetchone()
        if user:
            return (True, user)
        else:
            return (False, "No user with that name")
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# (Int, Int) -> List
def get_users(limit=None):
    if limit:
        req = g.db.execute('SELECT username, email, privilege FROM \
                            users ORDER BY username ASC LIMIT ?, ?',
                           [limit[0], limit[1]])
    else:
        req = g.db.execute('SELECT username, email, privilege FROM users \
                            ORDER BY username ASC')
    return req.fetchall()

# String, String, String, String -> (Bool, Maybe Error)
def insert_article(slug, title, content, posted):
    try:
        g.db.execute('INSERT INTO articles (slug, title, content) \
                      VALUES (?, ?, ?)', [slug, title, content])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String, String, String, String -> (Bool, Maybe Error)
def update_article(slug, title, content, posted):
    try:
        g.db.execute('UPDATE articles SET title=?, content=? \
                      WHERE slug=?', [title, content, slug])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Maybe Error)
def delete_article(slug):
    try:
        g.db.execute('DELETE FROM articles WHERE slug=?',
                     [slug])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Either List Error)
def get_article(slug):
    try:
        req = g.db.execute('SELECT title, content, posted FROM \
                            articles WHERE slug=?', [slug])
        article=req.fetchone()
        if article:
            return (True, article)
        else:
            return (False, "No article with that slug.")
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# (Int, Int) -> List
def get_articles(limit=None):
    if limit:
        req = g.db.execute('SELECT title, slug, content, posted FROM \
                            articles ORDER BY posted DESC LIMIT ?, ?',
                           [limit[0], limit[1]])
    else:
        req = g.db.execute('SELECT title, slug, content, posted \
                            FROM articles ORDER BY posted DESC')
    return req.fetchall()

# String, String, String -> (Bool, Maybe Error)
def insert_page(slug, title, content):
    try:
        g.db.execute('INSERT INTO pages (slug, title, content) \
                      VALUES (?, ?, ?)', [slug, title, content])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String, String, String -> (Bool, Maybe Error)
def update_page(slug, title, content):
    try:
        g.db.execute('UPDATE pages SET title=?, content=? \
                      WHERE slug=?', [title, content, slug])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Maybe Error)
def delete_page(slug):
    try:
        g.db.execute('DELETE FROM pages WHERE slug=?',
                     [slug])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Either List Error)
def get_page(slug):
    try:
        req = g.db.execute('SELECT title, content FROM \
                            pages WHERE slug=?', [slug])
        page=req.fetchone()
        if page:
            return (True, page)
        else:
            return (False, "No page with that slug.")
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# (Int, Int) -> List
def get_pages(limit=None):
    if limit:
        req = g.db.execute('SELECT title, slug, content FROM \
                            pages ORDER BY title ASC LIMIT ?, ?',
                           [limit[0], limit[1]])
    else:
        req = g.db.execute('SELECT title, slug, content FROM pages \
                            ORDER BY title ASC')
    return req.fetchall()