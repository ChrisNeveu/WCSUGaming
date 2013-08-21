from WCSUGaming import app, g, render_template, request, session, \
                       redirect, url_for, abort, flash, config
import WCSUGaming.database as Database

@app.before_request
def before_request():
    g.db = Database.connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def display_news():
    dbArticles = Database.get_articles(limit=(0,20))
    articles = [dict(title=row[0], slug=row[1],
                     content=row[2], posted=row[3])
                for row in dbArticles]
    return render_user_page('display_news.html',
                            articles=articles)
    
@app.route('/news/<slug>/')
def display_article(slug):
    result = Database.get_article(slug)
    if result[0]:
        article = dict(title=result[1][0], content=result[1][1],
                       posted=result[1][2])
        return render_user_page('display_article.html',
                                article=article)
    else:
        abort(404)
    
@app.route('/<slug>/')
def display_page(slug):
    result = Database.get_page(slug)
    if result[0]:
        page = dict(title=result[1][0], content=result[1][1])
        return render_user_page('display_page.html',
                                page=page)
    else:
        abort(404)

@app.route('/admin/')
def admin_home():
    if is_admin():
        return render_template('admin.html')
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/news/')
def display_admin_news():
    if is_admin():
        dbArticles = Database.get_articles(limit=(0,20))
        articles = [dict(title=row[0], slug=row[1], posted=row[3])
                    for row in dbArticles]
        return render_admin_page('admin_news.html', articles=articles)
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/news/new', methods=['GET', 'POST'])
def add_article():
    error = None
    if request.method == 'POST' and is_admin():
        result = Database.insert_article(request.form['slug'],
                                         request.form['title'],
                                         request.form['content'],
                                         0)
        if result[0]:
            flash('Post created.')
            return redirect(url_for('display_admin_news'))
        else:
            error = result[1]
    return render_admin_page('edit_article.html', error=error)

@app.route('/admin/news/edit/<slug>', methods=['GET', 'POST'])
def edit_article(slug):
    if request.method == 'POST' and is_admin():
        result = Database.update_article(slug,
                                         request.form['title'],
                                         request.form['content'],
                                         0)
        if result[0]:
            flash('Post created.')
            return redirect(url_for('display_admin_news'))
        else:
            return render_admin_page('edit_article.html', error=result[1])
    elif is_admin():
        result = Database.get_article(slug)
        if result[0]:
            article = dict(title=result[1][0], slug=slug,
                           content=result[1][1], posted=result[1][2])
            return render_admin_page('edit_article.html', article=article)
        else:
            return render_admin_page('edit_article.html', error=result[1])
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/news/bulk-edit', methods=['POST'])
def bulk_edit_articles():
    if request.method == 'POST' and is_admin():
        for slug in request.form.getlist('slugs'):
            Database.delete_article(slug)
    return redirect(url_for('display_admin_news'))

@app.route('/admin/pages/')
def display_admin_pages():
    if is_admin():
        dbPages = Database.get_pages(limit=(0,20))
        pages = [dict(title=row[0], slug=row[1])
                    for row in dbPages]
        return render_admin_page('admin_pages.html', pages=pages)
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/pages/new', methods=['GET', 'POST'])
def add_page():
    error = None
    if request.method == 'POST' and is_admin():
        result = Database.insert_page(request.form['slug'],
                                      request.form['title'],
                                      request.form['content'])
        if result[0]:
            flash('Page created.')
            return redirect(url_for('display_admin_pages'))
        else:
            error = result[1]
    return render_admin_page('edit_page.html', error=error)

@app.route('/admin/pages/edit/<slug>', methods=['GET', 'POST'])
def edit_page(slug):
    if request.method == 'POST' and is_admin():
        result = Database.update_page(slug,
                                      request.form['title'],
                                      request.form['content'])
        if result[0]:
            flash('Page created.')
            return redirect(url_for('display_admin_pages'))
        else:
            return render_admin_page('edit_page.html', error=result[1])
    elif is_admin():
        result = Database.get_page(slug)
        if result[0]:
            page = dict(title=result[1][0], slug=slug,
                        content=result[1][1])
            return render_admin_page('edit_page.html', page=page)
        else:
            return render_admin_page('edit_page.html', error=result[1])
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/pages/bulk-edit', methods=['POST'])
def bulk_edit_pages():
    if request.method == 'POST' and is_admin():
        for slug in request.form.getlist('slugs'):
            Database.delete_page(slug)
    return redirect(url_for('display_admin_pages'))

@app.route('/admin/users/')
def display_admin_users():
    if is_admin():
        req = Database.get_users(limit=(0,20))
        users = [dict(name=row[0], email=row[1], privilege=row[2])
                    for row in req]
        return render_admin_page('admin_users.html', users=users)
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/users/edit/<name>', methods=['GET', 'POST'])
def edit_user(name):
    if request.method == 'POST' and is_admin():
        result = Database.update_user(name,
                                      None,
                                      request.form['email'],
                                      request.form['privilege'])
        if result[0]:
            flash('User updated.')
            return redirect(url_for('display_admin_users'))
        else:
            return render_admin_page('edit_user.html', error=result[1])
    elif is_admin():
        result = Database.get_user(name)
        if result[0]:
            user = dict(name=name, email=result[1][1],
                        privilege=result[1][2])
            return render_admin_page('edit_user.html', user=user)
        else:
            return render_admin_page('edit_user.html', error=result[1])
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/users/bulk-edit', methods=['POST'])
def bulk_edit_users():
    if request.method == 'POST' and is_admin():
        for name in request.form.getlist('names'):
            Database.delete_user(name)
    return redirect(url_for('display_admin_users'))

@app.route('/login',methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        result = Database.validate_user(request.form['username'],
                                        request.form['password'])
        if result[0]:
            session['logged_in'] = True
            session['username'] = request.form['username']
            session['privilege'] = result[1]
            flash('You have been logged in')
            return redirect(url_for('display_news'))
        else:
            error = result[1]
    return render_user_page('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('privilege', None)
    flash('You have been logged out')
    return redirect(url_for('display_news'))

@app.route('/register', methods=['POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['password'] != request.form['password2']:
            error = "Passwords not the same"
        else:
            error = (Database.register_user(request.form['username'],
                                            request.form['password'],
                                            request.form['email']))[1]
    return render_user_page('login.html', error=error)

@app.route('/forum/')
def display_threads():
    '''Show latest threads.'''

@app.route('/forum/post-<int:pId>/')
def display_post():
    '''Show post with id pId and children.'''

@app.route('/forum/add', methods=['POST'])
def insert_thread():
    '''Add post.'''

def get_pages():
    req = Database.get_pages()
    return [dict(title=row[0], slug=row[1])for row in req]

def render_user_page(template, **kwargs):
    return render_template(template,
                           pages=get_pages(),
                           **kwargs)

def render_admin_page(template, **kwargs):
    return render_template(template,
                           ADMIN_LEVEL=config.ADMIN_LEVEL,
                           **kwargs)

def is_admin():
    return session.get('privilege', 0) >= config.ADMIN_LEVEL