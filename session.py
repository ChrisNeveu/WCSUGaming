from WCSUGaming import app, g, render_template, request, session, \
                       redirect, url_for, abort, flash, config

def log_in(name, email, privilege):
    session['logged_in'] = True
    session['name'] = name
    session['email'] = email
    session['privilege'] = privilege

def log_out():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('privilege', None)

def is_logged_in():
    return session.get('logged_in', False)
    
def is_admin():
    return session.get('privilege', 0) >= config.ADMIN_LEVEL

def get_name():
    return session.get('name', None)

def get_email():
    return session.get('email', None)