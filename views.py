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
    
@app.route('/p-<slug>/')
def display_page(slug):
    '''Show page with slug.'''

@app.route('/admin/')
def display_threads():
    '''Show admin page.'''

@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        user_pair = Database.validate_user(request.form['username'],
                                           request.form['password'])
        if user_pair is None:
            error = 'Invalid login'
        else:
            session['logged_in'] = True
            session['username'] = user_pair[0]
            session['privilege'] = user_pair[1]
            flash('You were logged in')
            return redirect(url_for('display_news'))
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
            error = Database.register_user(request.form['username'],
                                           request.form['password'],
                                           request.form['email'])
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