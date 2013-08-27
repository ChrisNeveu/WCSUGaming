from WCSUGaming import app, render_template, request, session, database, \
                       g, redirect, url_for, abort, flash, config, user, \
                       creole

@app.before_request
def before_request():
    g.db = database.connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def display_news():
    dbArticles = database.get_articles(limit=(0,20))
    articles = [dict(title=row[0], slug=row[1],
                     content=row[2], posted=row[3])
                for row in dbArticles]
    return render_user_page('display_news.html',
                            articles=articles)
    
@app.route('/news/<slug>/')
def display_article(slug):
    result = database.get_article(slug)
    if result[0]:
        article = dict(title=result[1][0], content=result[1][1],
                       posted=result[1][2])
        return render_user_page('display_article.html',
                                article=article)
    else:
        abort(404)
    
@app.route('/<slug>/')
def display_page(slug):
    result = database.get_page(slug)
    if result[0]:
        page = dict(title=result[1][0], content=result[1][1])
        return render_user_page('display_page.html',
                                page=page)
    else:
        abort(404)

@app.route('/admin/')
def admin_home():
    if user.is_admin():
        return render_admin_page('admin.html')
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/news/')
def display_admin_news():
    if user.is_admin():
        dbArticles = database.get_articles(limit=(0,20))
        articles = [dict(title=row[0], slug=row[1], posted=row[3])
                    for row in dbArticles]
        return render_admin_page('admin_news.html', articles=articles)
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/news/new', methods=['GET', 'POST'])
def add_article():
    error = None
    if request.method == 'POST' and user.is_admin():
        result = database.insert_article(request.form['slug'],
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
    if request.method == 'POST' and user.is_admin():
        result = database.update_article(slug,
                                         request.form['title'],
                                         request.form['content'],
                                         0)
        if result[0]:
            flash('Post created.')
            return redirect(url_for('display_admin_news'))
        else:
            return render_admin_page('edit_article.html', error=result[1])
    elif user.is_admin():
        result = database.get_article(slug)
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
    if request.method == 'POST' and user.is_admin():
        for slug in request.form.getlist('slugs'):
            database.delete_article(slug)
    return redirect(url_for('display_admin_news'))

@app.route('/admin/pages/')
def display_admin_pages():
    if user.is_admin():
        dbPages = database.get_pages(limit=(0,20))
        pages = [dict(title=row[0], slug=row[1])
                    for row in dbPages]
        return render_admin_page('admin_pages.html', pages=pages)
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/pages/new', methods=['GET', 'POST'])
def add_page():
    error = None
    if request.method == 'POST' and user.is_admin():
        result = database.insert_page(request.form['slug'],
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
    if request.method == 'POST' and user.is_admin():
        result = database.update_page(slug,
                                      request.form['title'],
                                      request.form['content'])
        if result[0]:
            flash('Page created.')
            return redirect(url_for('display_admin_pages'))
        else:
            return render_admin_page('edit_page.html', error=result[1])
    elif user.is_admin():
        result = database.get_page(slug)
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
    if request.method == 'POST' and user.is_admin():
        for slug in request.form.getlist('slugs'):
            database.delete_page(slug)
    return redirect(url_for('display_admin_pages'))

@app.route('/admin/users/')
def display_admin_users():
    if user.is_admin():
        req = database.get_users(limit=(0,20))
        users = [dict(name=row[0], email=row[1],
                      privilege=row[2], active=row[3])
                    for row in req]
        return render_admin_page('admin_users.html', users=users)
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/users/edit/<name>', methods=['GET', 'POST'])
def edit_user(name):
    if request.method == 'POST' and user.is_admin():
        result = database.update_user(name,
                                      None,
                                      request.form['email'],
                                      request.form['privilege'],
                                      request.form['active'])
        if result[0]:
            flash('User updated.')
            return redirect(url_for('display_admin_users'))
        else:
            return render_admin_page('edit_user.html', error=result[1])
    elif user.is_admin():
        result = database.get_user(name)
        if result[0]:
            theUser = dict(name=name, email=result[1][1],
                           privilege=result[1][2], active=result[1][3])
            return render_admin_page('edit_user.html', user=theUser)
        else:
            return render_admin_page('edit_user.html', error=result[1])
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/users/bulk-edit', methods=['POST'])
def bulk_edit_users():
    if request.method == 'POST' and user.is_admin():
        for name in request.form.getlist('names'):
            database.delete_user(name)
    return redirect(url_for('display_admin_users'))

@app.route('/login',methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        result = database.validate_user(request.form['username'],
                                        request.form['password'])
        if result[0]:
            user.log_in(request.form['username'],
                        result[1][0], result[1][1])
            flash('You have been logged in')
            return redirect(url_for('display_news'))
        else:
            error = result[1]
    return render_user_page('login.html', error=error)

@app.route('/logout')
def logout():
    user.log_out()
    flash('You have been logged out')
    return redirect(url_for('display_news'))

@app.route('/register', methods=['POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['password'] != request.form['password2']:
            error = "Passwords not the same"
        else:
            error = (database.register_user(request.form['username'],
                                            request.form['password'],
                                            request.form['email']))[1]
            if error is None:
                flash('Your account will be activated shortly.')
    return render_user_page('login.html', error=error)

@app.route('/forum/')
def display_threads():
    if user.is_logged_in():
        req = database.get_posts(limit=(0,20), parent=None)
        posts = [dict(id=row[0], title=row[1], content=row[2],
                      author=row[3], posted=row[4])
                    for row in req]
        return render_user_page('forum.html', posts=posts)
    else:
        return redirect(url_for('display_news'))

@app.route('/forum/<int:post_id>/')
def display_post(post_id):
    result = database.get_post(post_id)
    if result[0]:
        post = dict(id=result[1][0], title=result[1][1],
                    content=result[1][2], author=result[1][3],
                    posted=result[1][4], parent=result[1][5], 
                    children=get_children(result[1][0],config.NESTING))
        return render_user_page('display_post.html',
                                post=post)
    else:
        abort(404)

@app.route('/forum/new', methods=['GET', 'POST'])
def add_post():
    error = None
    if user.is_logged_in():
        if request.method == 'POST':
            result = database.insert_post(request.form['title'],
                                          request.form['content'],
                                          request.form['author'],
                                          0,
                                          None)
            if result[0]:
                flash('Post created.')
                return redirect(url_for('display_threads'))
            else:
                error = result[1]
        return render_user_page('edit_post.html', error=error)
    else:
        return redirect(url_for('display_news'))

@app.route('/forum/<int:parent_id>/reply', methods=['GET', 'POST'])
def add_reply(parent_id):
    error = None
    if user.is_logged_in():
        if request.method == 'POST':
            result = database.insert_post(request.form['title'],
                                          request.form['content'],
                                          request.form['author'],
                                          0,
                                          parent_id)
            if result[0]:
                flash('Post created.')
                return redirect(url_for('display_post', post_id=parent_id))
            else:
                error = result[1]
        return render_user_page('edit_post.html',
                                error=error, parent=parent_id)
    else:
        return redirect(url_for('display_news'))
            

@app.route('/forum/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if user.is_logged_in():
        result = database.get_post(post_id)
        post = dict(id=result[1][0], title=result[1][1],
                    content=result[1][2], author=result[1][3],
                    posted=result[1][4])
        if not result[0]:
            return render_user_page('edit_post.html', error=result[1])
        if (user.get_name() == post['author'] or user.is_admin()):
            if request.method == 'POST':
                result = database.update_post(post_id,
                                              request.form['title'],
                                              request.form['content'])
                if result[0]:
                    flash('Post Updated.')
                    return redirect(url_for(display_post('display_post',
                                                         post_id=post_id)))
                else:
                    return render_user_page('edit_post.html',
                                            error=result[1])
            else:
                return render_user_page('edit_post.html', post=post)
    else:
        return redirect(url_for('display_news'))
                
            
def get_pages():
    req = database.get_pages()
    return [dict(title=row[0], slug=row[1])for row in req]

def render_user_page(template, **kwargs):
    return render_template(template,
                           pages=get_pages(),
                           ADMIN_LEVEL=config.ADMIN_LEVEL,
                           **kwargs)

def render_admin_page(template, **kwargs):
    return render_template(template,
                           ADMIN_LEVEL=config.ADMIN_LEVEL,
                           **kwargs)

def get_children(post_id, levels):
    if levels > 0:
    	result = database.get_posts(parent=post_id)
        return [dict(id=row[0], title=row[1], content=row[2],
                     author=row[3], posted=row[4],
                     children=get_children(row[0], (levels - 1)))
                for row in result]
    else:
        return None