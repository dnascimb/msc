import uuid
from msc import app
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash
from sqlalchemy import func

import msc.view_service_request
import msc.view_user
import msc.view_customer

from msc.models import User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        session['logged_in'] = False
        session['user_id'] = None
        session['user_name'] = None
        return render_template('index_old.html')
    elif request.method == 'POST':
        if checkUserExists(request):
            cc_result = checkCredentials(request)
            if cc_result:
                session['logged_in'] = True
                session['user_id'] = cc_result
                session['user_name'] = User.query.filter_by(id=cc_result).first().name
                return redirect(url_for('home'))
        error = 'Invalid Login Credentials'
    
    return render_template('index.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

def checkCredentials(request):
    _inputEmail =  request.form['inputEmail']
    result = User.query.filter(func.lower(User.email) == func.lower(_inputEmail)).first()
    if not result:
        return False
    else:
        if result.check_password(request.form['inputPassword']):
            return result.id
        else:
            return 0
                
def checkUserExists(request):
    _inputEmail = request.form['inputEmail']
    result = User.query.filter(func.lower(User.email) == func.lower(_inputEmail)).first()

    if not result:
        return False
    else:
        return True

#
# determines if a user with the specified email exists
#
def checkEmailAvailable(request):
    _inputEmail = request.form['inputEmail']
    result = User.query.filter(func.lower(User.email) == func.lower(_inputEmail)).first()

    if not result:
        return True
    else:
        return False