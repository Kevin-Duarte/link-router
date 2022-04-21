
from datetime import datetime, timedelta
from email import message
from email.errors import MessageError
from email.policy import default
from inspect import isasyncgenfunction
from lib2to3.pytree import convert
from logging import exception
import time
import os
import re
import sys
from tkinter import E
from turtle import Turtle
from flask import Flask, Response, make_response, render_template, request, session, redirect, abort, jsonify
import sqlite3
from databaseHandler import databaseHandler
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import hashlib
import json
from smtpHandler import smtpHandler
import html
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Blueprint
import inspect
from waitress import serve


blacklist_keys = ['password', 'admin', 'user', 'anon', 'reset', 'sign', 'log', 'virus', 'free', 'money',
'urgent', 'porn', 'sex', 'child', 'cp', 'loli', 'illegal', 'xx', 'pass'
]

BAN_FAIL_AUTH = os.environ['BAN_FAIL_AUTH']
DEFAULT_ADMIN_EMAIL = os.environ['DEFAULT_ADMIN_EMAIL']
DEFAULT_ADMIN_PASSWORD = os.environ['DEFAULT_ADMIN_PASSWORD']
DATABASE_LOCATION = os.environ['DATABASE_LOCATION']
DATABASE_FILENAME = os.environ['DATABASE_FILENAME']

database = databaseHandler(DATABASE_LOCATION, DATABASE_FILENAME, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD)
HOST_BASE = os.environ['HOST_BASE']
smtp = smtpHandler(
    SERVER=os.environ['SMTP_SERVER'],
    USERNAME=os.environ['SMTP_USERNAME'],
    PASSWORD=os.environ['SMTP_PASSWORD'],
    BCC_COPY=os.environ['SMTP_BCC_COPY']
)

app = Flask(__name__, template_folder='template')
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['4 per second']
)


app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['TEMPLATES_AUTO_RELOAD'] = True


login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, email, password, accountActive, firstName, lastName, admin, disabled):
        self.id = id
        self.email = email
        self.password = password
        self.accountActive = accountActive
        self.authenticated = True
        self.firstName = firstName
        self.lastName = lastName
        self.admin = admin
        self.disabled = disabled
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
       return self.accountActive

    def get_id(self):
        return self.id

# load user
@login_manager.user_loader
def load_user(user_id):
    user = database.getUser(user_id)
    if user is None:
        return None
    return User(int(user['id']), user['email'], user['password'], bool(user['accountActive']), user['firstName'], user['lastName'], bool(user['admin']), bool(user['disabled']))

# choke-point for adding links
def validateAndAddLink(key, link, createdBy, expiration):
    if not re.fullmatch(r'^[a-zA-Z0-9_-]+$', key) or not re.fullmatch(r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*$)', link):
        raise Exception("Link contains illegal characters")

    if database.existsLinkKey(key):
        raise Exception("Link is already taken")

    if any(substring in key for substring in blacklist_keys):
        raise Exception("Link is not allowed")
    
    if link.startswith('https://') == False and link.startswith('http://') == False:
        link = 'http://' + link
    
    return database.addLink(key, link, createdBy, expiration)

# Choke point for setting passwords
def validateAndSetPassword(userId, newPassword):
    if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', newPassword):
        raise Exception("Password complexity not met")
    database.setUserPassword(userId, newPassword)

# Choke point for getting ip address
def getIPAddr():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


# Before request settings
@app.before_request
def beforeRequest():

    bannedList = database.getBannedList()
    bannedListIPs = [ x['ipaddr'] for x in bannedList]
    if getIPAddr() in bannedListIPs:
        database.addEvent('BANNED_VISIT', getIPAddr(), -1, "Banned visitor attempted to visit")
        return '',404

    # disabled account checks
    try:
        if current_user.disabled == True:
            current_user.authenticated = False
            logout_user()
            cookieInject.delete_cookie('loggedIn')
            cookieInject.delete_cookie('admin')
    except:
        pass

    # inactive account checks
    try:
        if current_user.accountActive == False:
            current_user.authenticated = False
            logout_user()
            cookieInject = make_response(jsonify(message='Successfully logged out'))
            cookieInject.delete_cookie('loggedIn')
            cookieInject.delete_cookie('admin')
            return cookieInject, 200
    except:
        pass

    # Clean up old database links 
    try:
        database.cleanUpLinks()
    except:
        pass

    # Clean up old database events 
    try:
        database.cleanUpEvents()
    except:
        pass


# Exception handler
@app.errorhandler(Exception)
def all_exception_handler(error):
    isAuthenticated = False
    try:
        isAuthenticated = current_user.is_authenticated()
    except:
        pass

    if isAuthenticated == True:
        database.addEvent('EXCEPTION', getIPAddr(), current_user.get_id(), "Error: " + str(error))
    else:
        database.addEvent('EXCEPTION', getIPAddr(), -1, "Error " + inspect.trace()[-1][3] + ": " + str(error))
        
    return jsonify(message = str(error)), 400


# Decorators
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
            isAdmin = False
            try:
                isAdmin = current_user.admin
            except:
                pass

            if isAdmin == False:
                raise Exception("Admin rights required")
            return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
            isAuthenticated = False
            try:
                isAuthenticated = current_user.is_authenticated()
            except:
                pass

            if isAuthenticated == False:
                raise Exception("Login required")
            return f(*args, **kwargs)
    return decorated_function