from WCSUGaming import app, g, render_template, request, session, \
                       redirect, url_for, abort, flash, config, database
import time
from os import urandom
from base64 import b64encode

def log_in(name, email, privilege, last_login):
    session['logged_in'] = True
    session['name'] = name
    session['email'] = email
    session['privilege'] = privilege
    session['last_login'] = last_login

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

def persist_login(response):
    token = b64encode(urandom(64))
    series_id = b64encode(urandom(64))
    response.set_cookie('persist_name', session['name'], 1210000)
    response.set_cookie('persist_token', token, 1210000)
    response.set_cookie('persist_id', series_id, 1210000)
    database.insert_persist_login(session['name'], token, series_id)

def auto_log_in():
    name = request.cookies.get('persist_name', None)
    token = request.cookies.get('persist_token', None)
    series_id = request.cookies.get('persist_id', None)
    if name and token and series_id:
        logins = database.get_persist_logins(name)
        for login in logins:
            if token == login[1] and series_id == login[2]:
                user = database.get_user(name)
                log_in(name, user[1][1], user[1][2], user[1][4])
                new_token = b64encode(urandom(64))
                database.update_persist_login(token, new_token)
                return new_token
            elif series_id == login[2]:
                database.delete_persist_login(series_id)
                flash('It appears your user session has been hijacked, \
                       please ensure that your browser is secure.')
    return None