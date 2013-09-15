import bcrypt
import sqlite3
import peewee as pw
from WCSUGaming import app, g
from contextlib import closing
from datetime import datetime

def init_db():
    User.create_table()
    Page.create_table()
    Post.create_table()
    admin = User.create(
        name='admin',
        password=bcrypt.hashpw('password', bcrypt.gensalt()),
        email='mail@test.com',
        privilege=4,
        active=True
    )

def connect_db():
    return pw.PostgresqlDatabase(app.config['DB_NAME'],
                                 host=app.config['DB_HOST'],
                                 user=app.config['DB_USER'],
                                 password=app.config['DB_PASS'])

db = connect_db()

class BaseModel(pw.Model):
    class Meta:
        database = db

class User(BaseModel):
    name = pw.CharField(primary_key=True)
    password = pw.CharField()
    email = pw.CharField()
    privilege = pw.IntegerField(default=0)
    last_login = pw.DateTimeField(default=datetime.utcnow())
    active = pw.BooleanField(default=False)

    class Meta:
        order_by = ('name',)

    def validate(self, passw):
        if not self.active:
            return (False, "User not activated")
        if bcrypt.hashpw(passw, self.password) == self.password:
            return (True, None)
        else:
            return (False, "Incorrect Password")

class Page(BaseModel):
    slug = pw.CharField(primary_key=True)
    title = pw.CharField()
    content = pw.TextField()

    class Meta:
        order_by = ('title',)

class Post(BaseModel):
    post_id = pw.PrimaryKeyField()
    title = pw.CharField(null=True)
    slug = pw.CharField(null=True)
    content = pw.TextField()
    author = pw.ForeignKeyField(User, related_name='posts')
    posted = pw.DateTimeField(default=datetime.utcnow())
    parent = pw.ForeignKeyField('self', related_name='children', null=True)
    locked = pw.BooleanField(default=False)
    pinned = pw.BooleanField(default=False)
    featured = pw.BooleanField(default=False)

    class Meta:
        order_by = ('-posted',)

def validate_user(username, password):
    try:
        user = User.get(User.name == username)
        if not user.active:
            return (False, "User not activated")
        if user.validate(password):
            return (True, [user.email, user.privilege,
                           user.last_login, user.active])
        else:
            return (False, "Incorrect Password")
    except User.DoesNotExist:
        return (False, "User not found.")

def register_user(username, password, email):
    try:
        user = User.get(User.name == username)
        return (False, 'Username is taken')
    except User.DoesNotExist:
        user = User.create(
            name=username,
            password=bcrypt.hashpw(password, bcrypt.gensalt()),
            email=email
        )
        return (True, None)

def update_user(username, password, email, privilege, active):
    try:
        user = User.get(User.name == username)
        user.email = email
        user.privilege = privilege
        user.active = active
        if password is not None:
            user.password = bcrypt.hashpw(password, bcrypt.gensalt())
        user.save()
        return (True, None)
    except User.DoesNotExist:
        return (False, "User not found.")

def activate_user(username):
    try:
        user = User.get(User.name == username)
        user.active = True
        user.save()
        return (True, None)
    except User.DoesNotExist:
        return (False, "User not found.")

def delete_user(username):
    try:
        user = User.get(User.name == username)
        user.delete_instance()
        return (True, None)
    except User.DoesNotExist:
        return (False, "User not found.")

def get_user(username):
    try:
        user = User.select().where(User.name == username).get()
        return (True, [user.name, user.email,
                       user.privilege, user.active])
    except User.DoesNotExist:
        return (False, "User not found")

def get_users(limit=None):
    users = []
    if limit:
        for user in User.select().offset(limit[0]).limit(limit[1]-limit[0]):
            users.append([user.name, user.email,
                          user.privilege, user.active])
    else:
        for user in User.select():
            users.append([user.name, user.email,
                          user.privilege, user.active])
    return users

def get_num_users():
    return User.select().count()

def insert_article(slug, title, content, posted):
    try:
        article = Post.get(Post.slug == slug)
        return (False, 'Slug is taken')
    except Post.DoesNotExist:
        article = Post.create(
            slug=slug,
            title=title,
            content=content,
            author='admin',
            featured=True
        )
        return (True, None)

def update_article(slug, title, content, posted):
    try:
        article = Post.get(Post.slug == slug)
        article.title = title
        article.content = content
        article.save()
        return (True, None)
    except Post.DoesNotExist:
        return (False, "Article not found.")

def delete_article(slug):
    try:
        article = Post.get(Post.slug == slug)
        article.delete_instance()
        return (True, None)
    except Post.DoesNotExist:
        return (False, "Article not found.")

def get_article(slug):
    try:
        article = Post.select().where(Post.slug == slug).get()
        return (True, [article.title, article.content,
                       article.posted])
    except Post.DoesNotExist:
        return (False, "Article not found")

def get_articles(limit=None):
    articles = []
    if limit:
        for article in Post.select().where(Post.featured == True).offset(limit[0]).limit(limit[1] - limit[0]):
            articles.append([article.title, article.slug,
                             article.content, article.posted])
    else:
        for article in Post.select().where(Post.featured == True):
            articles.append([article.title, article.slug,
                             article.content, article.posted])
    return articles

def get_num_articles():
    return Post.select().where(Post.featured == True).count()

def insert_page(slug, title, content):
    try:
        page = Page.get(Page.slug == slug)
        return (False, 'Slug is taken')
    except Page.DoesNotExist:
        page = Page.create(
            slug=slug,
            title=title,
            content=content
        )
        return (True, None)

def update_page(slug, title, content):
    try:
        page = Page.get(Page.slug == slug)
        page.title = title
        page.content = content
        page.save()
        return (True, None)
    except Page.DoesNotExist:
        return (False, "Page not found.")

def delete_page(slug):
    try:
        page = Page.get(Page.slug == slug)
        page.delete_instance()
        return (True, None)
    except Page.DoesNotExist:
        return (False, "Page not found.")
        
def get_page(slug):
    try:
        page = Page.select().where(Page.slug == slug).get()
        return (True, [page.title, page.content])
    except Page.DoesNotExist:
        return (False, "Page not found")

def get_pages(limit=None):
    pages = []
    if limit:
        for page in Page.select().offset(limit[0]).limit(limit[1] - limit[0]):
            pages.append([page.title, page.slug, page.content])
    else:
        for page in Page.select():
            pages.append([page.title, page.slug, page.content])
    return pages

def get_num_pages():
    return Page.select().count()

def insert_post(title, content, author, posted, parent, pinned):
    post = Post.create(
        title=title,
        content=content,
        author=author,
        parent=parent,
        pinned=pinned
    )
    return (True, None)

def update_post(post_id, title, content, lock, pinned):
    try:
        post = Post.get(Post.post_id == post_id)
        post.title = title
        post.content = content
        post.locked = lock
        post.pinned = pinned
        post.save()
        return (True, None)
    except Post.DoesNotExist:
        return (False, "Post not found.")

def delete_post(post_id):
    try:
        post = Post.get(Post.post_id == post_id)
        post.delete_instance()
        return (True, None)
    except Post.DoesNotExist:
        return (False, "Post not found.")

def get_post(post_id):
    try:
        post = Post.select().where(Post.post_id == post_id).get()
        if post.parent:
            parent_id = post.parent.post_id
        else:
            parent_id = None
        return (True, [post_id, post.title, post.content, post.author.name, 
                       post.posted, parent_id, post.locked,
                       post.pinned])
    except Post.DoesNotExist:
        return (False, "Post not found")

def get_posts(limit=None, parent=False, order='DESC'):
    posts = []
    if limit and parent is not False and order is 'ASC':
        query = Post.select().offset(limit[0]).limit(limit[1] - limit[0]).where(Post.parent >> parent).order_by(Post.posted.asc)
    elif limit and parent is not False:
        query = Post.select().offset(limit[0]).limit(limit[1] - limit[0]).where(Post.parent >> parent)
    elif limit and order is 'ASC':
        query = Post.select().offset(limit[0]).limit(limit[1] - limit[0]).order_by(Post.posted.asc)
    elif parent is not False and order is 'ASC':
        query = Post.select().where(Post.parent >> parent).order_by(Post.posted.asc)
    elif limit:
        query = Post.select().offset(limit[0]).limit(limit[1] - limit[0])
    elif parent is not False:
        query = Post.select().where(Post.parent >> parent)
    elif order is 'ASC':
        query = Post.select().order_by(Post.posted.asc)
    else:
        query = Post.select()
    for post in query:
        posts.append([post.post_id, post.title, post.content,
                      post.author.name, post.posted, post.locked,
                      post.pinned])
    return posts

def get_num_posts(parent=False):
    if parent is False:
        return Post.select().count()
    else:
        return Post.select().where(Post.parent == parent).count()