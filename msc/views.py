import uuid
from msc import app
from msc.database import db_session
from msc.models import User
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash
from sqlalchemy import func


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

@app.route('/new_user_request', methods=['GET'])
def new_user_request():
    return render_template('signup.html')

@app.route('/create_user_request', methods=['POST'])
def create_user_request():
    error = None
    if not validUserRequest(request):
        error = 'Invalid data entered'
        print('invalid data entered')
        return render_template('signup.html', error=error)

    print('start add proces...')
    user_name = request.form['inputName']
    print("name is: " + user_name)
    password = request.form['inputPassword']
    print("password is: " + password)
    password2 = request.form['inputPassword2']
    print("password2 is: " + password2)
    user_company = request.form['inputCompanyName']
    print("company: " + user_company)
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
    country = request.form['inputCountry']
    print("Country: " + country)
    zipc = request.form['inputZip']
    print("zip: " + zipc)

    if not checkEmailAvailable(request):
        error = 'Sorry, that email is already taken'
        print('email in use')
        return render_template('signup.html',  retUserName=user_name, retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, retCity=city, retState=state, retZip=zip, retCountry=country, error=error)
    
    i = str(uuid.uuid4())

    session['userid'] = i
    
    print('session ID in USER ADD--', session['userid'])

    if password == password2:
        hashedPassword = User(i, password)
        updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        u = User(i, user_name, hashedPassword, user_company, email, phone, streetAddress1, streetAddress2, city, state, zipc, country, updated_at)

        #db.execute('insert into user_profiles (id, user_name, user_company, email, phone, address1, address2, city, state, zip, country, updated_at, password) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [i, user_name, user_company, email, phone, streetAddress1, streetAddress2, city, state, zip, country, updated_at, hashedPassword])
        #db.commit()
        flash('New user was successfully added')
        return redirect(url_for('home'))
    else:
        print('unsuccessful add')
        error="passwords do not match"
        return render_template('signup.html', retUserName=user_name, retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, retCity=city, retState=state, retZip=zip, retCountry=country, error=error)

    

@app.route('/view_user_request', methods=['GET'])
def view_user_request():

    print("in view_user_request function - request method: " + request.method)

    db = get_db()

    user_profile = db.cursor()
 
    the_user =  session['userid']
    sql = "select id, user_name, user_company, email, phone, address1, address2, city, state, zip, country from user_profiles where id = ?"
    user_profile.execute(sql, [the_user])
    
    # print 'return from call:  ', user_profile.fetchone()  # or use fetchall()
    
    id, user_name, user_company, email, phone, streetAddress1, streetAddress2, city, state, zip, country = user_profile.fetchone()

    #print("name: " + user_name)
    #print("company: " + user_company)
    #print("phone: " + phone)
    #print("email: " + email)
    #print("street address 1: " + streetAddress1)
    #rint("street address 2: " + streetAddress2)
    #print("city: " + city)
    #print("State: " + state)    
    #print("Country: " + country)
    #print("zip: " + zip)
    
    fromProfile = True
    return render_template('customer_profile.html', fromProfile=fromProfile, retUserName=user_name, retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, retCity=city, retState=state, retZip=zip, retCountry=country)
       
@app.route('/view_user_request', methods=['post'])
def update_user_request():

    print("in update_user_request function - request method: " + request.method)

    fromProfile = True

    user_name = request.form['inputName']
    print("name is: " + user_name)
    user_company = request.form['inputCompanyName']
    print("company: " + user_company)
    phone = request.form['inputPhone']
    print("phone: " + phone)
    email = request.form['inputEmail']
    print("email: " + email)   
    password = request.form['inputPassword']
    print("password1: " + password)
    password2 = request.form['inputPassword2']
    print("password2: " + password2)    
    streetAddress1 = request.form['inputStreetAddress1']
    print("street address 1: " + streetAddress1)
    streetAddress2 = request.form['inputStreetAddress2']
    print("street address 2: " + streetAddress2)
    city = request.form['inputCity']
    print("city: " + city)
    state = request.form['inputState']
    print("State: " + state)    
    country = request.form['inputCountry']
    print("Country: " + country)
    zip = request.form['inputZip']
    print("zip: " + zip)

    getUser =  session['userid']
    print('session ID in UPDATE--', session['userid'])

    updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    db = get_db()

    if len(password) != 0:
        if password != password2:
            error = 'passwords do not match'
            return render_template('customer_profile.html', fromProfile=fromProfile, retUserName=user_name, retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, retCity=city, retState=state, retZip=zip, retCountry=country, error=error)
        else:
            hashedPassword = hashAPassword(getUser, password)
            try:
                db.execute('update user_profiles set password=?, updated_at=? where id=?', [hashedPassword, updated_at, getUser])
                db.commit()
            except sqlite3.Error as e:
                print("An error occurred:", e.args[0])

    try:
        db.execute('update user_profiles set user_name=?, user_company=?, email=?, phone=?, address1=?, address2=?, city=?, state=?, zip=?, country=?, updated_at=? where id=?', [user_name, user_company, email, phone, streetAddress1, streetAddress2, city, state, zip, country, updated_at, getUser])
        db.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

    flash('User was successfully updated')
    
    # print 'return from call:  ', user_profile.fetchone()  # or use fetchall()
   
    return render_template('customer_profile.html', fromProfile=fromProfile, retUserName=user_name, retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, retCity=city, retState=state, retZip=zip, retCountry=country)


def checkCredentials(request):

    db = get_db()

    user_login = db.cursor()
 
    the_user =  request.form['inputEmail']
    sql = "select id, password from user_profiles where email = ?"

    dbError=False

    try:
        user_login.execute(sql, [the_user])
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        dbError=True
    
    if dbError:
        return False
    else:
        id, password = user_login.fetchone()
        if check_password_hash(password, request.form['inputPassword']):
            session['userid'] = id
            print('session ID in CHECK CREDENTIALS--', session['userid'])
            return True
        else:
            return False
                
def checkUserExists(request):
    
    db = get_db()

    user_exist = db.cursor()
 
    the_user =  request.form['inputEmail']
    sql = "select count(*) from user_profiles where email = ?"

    dbError=False

    try:
        user_exist.execute(sql, [the_user])
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        dbError=True
        return False

    numberOfRows = user_exist.fetchone()[0]

    #print('record count is:' , numberOfRows)

    if numberOfRows == 0:
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
        print("User email query result: " + result)
        return False

#
# Hashes a password
#
def hashAPassword(userID, passToHash):

    return passToHash


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


def validUserRequest(request):
    # TODO
    return True


