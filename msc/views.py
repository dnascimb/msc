import uuid
from msc import app
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash
from sqlalchemy import func

#import views
import msc.view_service_request
import msc.view_user
import msc.view_customer

#import models
from msc.models import User

@app.route('/')
def index():
    #db = get_db()
    #cur = db.execute('select title, text from entries order by id desc')
    #entries = cur.fetchall()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if checkUserExists(request):
            if checkCredentials(request):
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                error = 'Invalid Login Credentials'
        else:
            error = 'Email address is not on file'
    
    return render_template('index.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    #flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/home')
def home():
#    db = get_db()
#    cur = db.execute('select uuid, number, type, status, updated_at, provider from service_requests order by number desc')
#    entries = cur.fetchall()
    return render_template('service_request_listing.html')


def checkCredentials(request):
 
    _inputEmail =  request.form['inputEmail']
    
    result = User.query.filter(func.lower(User.email) == func.lower(_inputEmail)).first()
    if not result:
        return False
    else:
        if result.check_password(request.form['inputPassword']):
            session['userid'] = result.id
           # print('session ID in CHECK CREDENTIALS--', session['userid'])
            return True
        else:
            return False
                
def checkUserExists(request):
    
    _inputEmail = request.form['inputEmail']

    result = User.query.filter(func.lower(User.email) == func.lower(_inputEmail)).first()

    if not result:
        return False
    else:
        return True



