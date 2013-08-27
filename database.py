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

# String, String -> (Bool, Either List Error)
def validate_user(username, password):
    try:
        req = g.db.execute('SELECT password, email, privilege, active \
                            FROM users WHERE username=?', [username])
        user = req.fetchone()
        if not user[3]:
            return (False, "User not activated")
        if user and bcrypt.hashpw(password, user[0]) == user[0]:
            return (True, user[1:3])
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

# String, String, String, Int -> (Bool, Maybe Error)
def update_user(username, password, email, privilege, active):
    try:
        if password is None:
            g.db.execute('UPDATE users SET email=?, privilege=?, active=? \
                          WHERE username=?',
                         [email, privilege, active, username])
        else:
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            g.db.execute('UPDATE users SET password=?, \
                          email=?, privilege=?, active=? \
                          WHERE username=?',
                         [hashed, email, privilege, active, username])
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
        req = g.db.execute('SELECT username, email, privilege, active \
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
        req = g.db.execute('SELECT username, email, privilege, active \
                            FROM users ORDER BY username ASC LIMIT ?, ?',
                           [limit[0], limit[1]])
    else:
        req = g.db.execute('SELECT username, email, privilege, active \
                            FROM users ORDER BY username ASC')
    return req.fetchall()

# String, String, String, Datetime -> (Bool, Maybe Error)
def insert_article(slug, title, content, posted):
    try:
        g.db.execute('INSERT INTO posts \
                      (slug, title, content, author, featured) \
                      VALUES (?, ?, ?, "admin", 1)', [slug, title, content])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String, String, String, Datetime -> (Bool, Maybe Error)
def update_article(slug, title, content, posted):
    try:
        g.db.execute('UPDATE posts SET title=?, content=? \
                      WHERE slug=?', [title, content, slug])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Maybe Error)
def delete_article(slug):
    try:
        g.db.execute('DELETE FROM posts WHERE slug=?',
                     [slug])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Either List Error)
def get_article(slug):
    try:
        req = g.db.execute('SELECT title, content, posted FROM \
                            posts WHERE slug=? AND featured=1', [slug])
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
                            posts WHERE featured=1 \
                            ORDER BY posted DESC LIMIT ?, ?',
                           [limit[0], limit[1]])
    else:
        req = g.db.execute('SELECT title, slug, content, posted \
                            FROM posts WHERE featured=1 \
                            ORDER BY posted DESC')
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

# String, String, String, Datetime, Int -> (Bool, Maybe Error)
def insert_post(title, content, author, posted, parent):
    try:
        g.db.execute('INSERT INTO posts \
                      (title, content, author, parent) \
                      VALUES (?, ?, ?, ?)',
                     [title, content, author, parent])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# Int, String, String -> (Bool, Maybe Error)
def update_post(post_id, title, content):
    try:
        g.db.execute('UPDATE posts SET title=?, content=? \
                      WHERE id=?', [title, content, post_id])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Maybe Error)
def delete_post(post_id):
    try:
        g.db.execute('DELETE FROM posts WHERE id=?',
                     [post_id])
        g.db.commit()
        return (True, None)
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# String -> (Bool, Either List Error)
def get_post(post_id):
    try:
        req = g.db.execute('SELECT \
                            id, title, content, author, posted, parent \
                            FROM posts WHERE id=?', [post_id])
        post =req.fetchone()
        if post:
            return (True, post)
        else:
            return (False, "No post with that id.")
    except sqlite3.Error as e:
        return (False, "An error occurred: " + e.args[0])

# (Int, Int), Int, Either DESC ASC -> List
def get_posts(limit=None, parent=False, order='DESC'):
    if not order == 'DESC' and not order == 'ASC':
        order = 'DESC'
    if limit and parent is not False:
        req = g.db.execute('SELECT \
                            id, title, content, author, posted \
                            FROM posts WHERE parent IS ? \
                            ORDER BY posted ' + order + ' LIMIT ?, ?',
                           [parent, limit[0], limit[1]])
    elif parent is not False:
        req = g.db.execute('SELECT \
                            id, title, content, author, posted \
                            FROM posts WHERE parent IS ? \
                            ORDER BY posted ' + order,
                           [parent])
    elif limit:
        req = g.db.execute('SELECT \
                            id, title, content, author, posted \
                            FROM posts ORDER BY posted ' + order +
                           ' LIMIT ?, ?',
                           [limit[0], limit[1]])
    else:
        req = g.db.execute('SELECT \
                            id, title, content, author, posted \
                            FROM posts ORDER BY posted ' + order)
    return req.fetchall()