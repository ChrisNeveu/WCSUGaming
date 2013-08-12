from WCSUGaming import app

@app.route('/')
def display_news():
    '''Show latest news.'''
    return "Test"
    
@app.route('/news/<slug>/')
def display_article():
    '''Show article with slug.'''
    
@app.route('/<slug>/')
def display_page():
    '''Show page with slug.'''

@app.route('/admin/')
def display_threads():
    '''Show admin page.'''

@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    '''Log user out.'''

@app.route('/register')
def register():
    '''Log user out.'''

@app.route('/forum/')
def display_threads():
    '''Show latest threads.'''

@app.route('/forum/post-<int:pId>/')
def display_post():
    '''Show post with id pId and children.'''

@app.route('/forum/add', methods=['POST'])
def insert_thread():
    '''Add post.'''