from datetime import datetime, timedelta
import sys
from tkinter import E
from turtle import Turtle
from xmlrpc.client import ProtocolError
from flask import Flask, Response, appcontext_popped, make_response, render_template, request, session, redirect, abort, jsonify
from databaseHandler import databaseHandler
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from global_config import *
from api_anon import api_anon
from api_user import api_user
from api_admin import api_admin


# Importing restful APIs
app.register_blueprint(api_anon)
app.register_blueprint(api_user)
app.register_blueprint(api_admin)


### Webpage routes
@app.route("/set_password", methods=['GET'])
def set_password():
    return render_template('set_password.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    if path:
        
        query = database.getLinkByKey(path)
        if (query):
            realURL = query['realURL']
            database.addEvent('ROUTE', getIPAddr(), -1, html.escape(path) + " -> " + html.escape(realURL))
            return redirect(query['realURL'], code=302)
    database.addEvent('HOMEPAGE', getIPAddr(), -1, 'path: ' + path)
    return render_template('index.html')


#print("Application started", file=sys.stdout)
#print('This is error output test', file=sys.stderr)


if (__name__) == '__main__':
    #app.run(host='0.0.0.0', debug=False, port=80)
    serve(app, host='0.0.0.0', port=80)