from WCSUGaming import app, g, render_template, request, session, \
                       redirect, url_for, abort, flash
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
    return render_template('display_news.html')
    
@app.route('/news/<slug>/')
def display_article():
    '''Show article with slug.'''
    
@app.route('/<slug>/')
def display_page(slug):
    '''Show page with slug.'''

@app.route('/admin/')
def admin_home():
    '''Show admin page.'''

@app.route('/admin/news/')
def display_admin_news():
    '''Show article list.'''
    if session.get('logged_in', None):
        dbArticles = Database.get_articles(limit=(0,20))
        articles = [dict(title=row[0], slug=row[1], posted=row[3])
                    for row in dbArticles]
        return render_template('admin_news.html', articles=articles)
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/news/new', methods=['GET', 'POST'])
def add_article():
    error = None
    if request.method == 'POST' and session.get('logged_in', None):
        result = Database.insert_article(request.form['slug'],
                                         request.form['title'],
                                         request.form['content'],
                                         0)
        if result[0]:
            flash('Post created.')
            return redirect(url_for('display_admin_news'))
        else:
            error = result[1]
    return render_template('edit_article.html', error=error)

@app.route('/admin/news/edit/<slug>', methods=['GET', 'POST'])
def edit_article(slug):
    if request.method == 'POST' and session.get('logged_in', None):
        result = Database.update_article(slug,
                                         request.form['title'],
                                         request.form['content'],
                                         0)
        if result[0]:
            flash('Post created.')
            return redirect(url_for('display_admin_news'))
        else:
            return render_template('edit_article.html', error=result[1])
    elif session.get('logged_in', None):
        result = Database.get_article(slug)
        if result[0]:
            article = dict(title=result[1][0], slug=slug,
                           content=result[1][1], posted=result[1][2])
            return render_template('edit_article.html', article=article)
        else:
            return render_template('edit_article.html', error=result[1])
    else:
        return redirect(url_for('display_news'))

@app.route('/admin/pages/')
def display_admin_pages():
    '''Show page list.'''

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
            flash('You were logged in')
            return redirect(url_for('display_news'))
        else:
            error = result[1]
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
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
    return render_template('login.html', error=error)

@app.route('/forum/')
def display_threads():
    '''Show latest threads.'''

@app.route('/forum/post-<int:pId>/')
def display_post():
    '''Show post with id pId and children.'''

@app.route('/forum/add', methods=['POST'])
def insert_thread():
    '''Add post.'''