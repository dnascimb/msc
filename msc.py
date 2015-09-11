# -*- coding: utf-8 -*-
"""
    MSC
    ~~~~~~

    An example service request application using Flask.

    :copyright: (c) 2015 by Dan Nascimbeni.

"""

import os
import uuid
from datetime import datetime
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create the application
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'msc.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('MSC_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


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
        if request.form['inputUsername'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['inputPassword'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    
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


@app.route('/new_service_request', methods=['GET'])
def new_service_request():
    if not session.get('logged_in'):
        abort(401)
    return render_template('new_service_request.html')


@app.route('/create_service_request', methods=['POST'])
def create_service_request():
    if not session.get('logged_in'):
        abort(401)

    error = None
    if not validServiceRequest(request):
        error = 'Invalid data entered'
        return render_template('new_service_request.html', error=error)

    saveRequest(request)
    return redirect(url_for('home'))


def validServiceRequest(request):
    # TODO
    return True

def saveRequest(request):
    warranty = request.form.getlist('checkboxes')
    #print("warranty: " + warranty)
    vendor = ''
    print("vendor: " + vendor)
    troubleshoot = ''
    print("troubleshoot: " + troubleshoot)
    contact_name = request.form['inputContactName']
    print("contact_name: " + contact_name)
    contact_phone = request.form['inputContactPhone']
    print("contact_phone: " + contact_phone)
    contact_email = request.form['inputContactEmail']
    print("contact_email: " + contact_email)
    manufacturer = request.form['inputEquipmentManufacturer']
    print("manufacturer: " + manufacturer)
    model = request.form['inputEquipmentModel']
    print("model: " + model)
    date_purchased = request.form['inputEquipmentDatePurchased']
    print("date_purchased: " + date_purchased)
    appointment = request.form['inputTimeframe']
    print("appointment: " + appointment)
    description = request.form['inputDescription']
    print("description: " + description)

    db = get_db()
    i = str(uuid.uuid4())
    number = 3830238
    rtype = 'Service'
    status = 'Open'
    updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    provider = 'Advantage'

    db.execute('insert into service_requests (id, number, type, status, updated_at, provider) values (?, ?, ?, ?, ?, ?)',
               [i, number, rtype, status, updated_at, provider])
    db.commit()
    flash('New request was successfully submitted')

    return True

@app.route('/new_user_request', methods=['GET'])
def new_user_request():

    if not session.get('logged_in'):
        abort(401)
    return render_template('profile_manager.html')

@app.route('/create_user_request', methods=['POST'])
def create_user_request():
    if not session.get('logged_in'):
        abort(401)

    error = None
    if not validUserRequest(request):
        error = 'Invalid data entered'
        return render_template('profile_manager.html', error=error)

    saveProfile(request)
    return render_template('profile_manager.html', error=error)

def validUserRequest(request):
    # TODO
    return True
	
def saveProfile(request):
    user_name = request.form['inputName']
    print("name: " + user_name)
    phone = request.form['inputPhone']
    print("phone: " + phone)
    email = request.form['inputEmail']
    print("email: " + email)
    streetAddress1 = request.form['inputStreetAddress1']
    print("street address 1: " + streetAddress1)
    streetAddress2 = request.form['inputStreetAddress2']
    print("street address 2: " + streetAddress2)
    city = request.form['inputCity']
    print("city: " + city)
    state = request.form['inputState']
    print("State: " + state)
    zip = request.form['inputZip']
    print("zip: " + zip)

    db = get_db()
    i = str(uuid.uuid4())
    updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    db.execute('insert into user_profiles (id, user_name, email, phone, address1, address2, city, state, zip, updated_at) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
               [i, user_name, email, phone, streetAddress1, streetAddress2, city, state, zip, updated_at])
    db.commit()
    flash('New user was successfully added')

    return True
	
if __name__ == "__main__":
  app.run()
