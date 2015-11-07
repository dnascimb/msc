import uuid
from msc import app
from msc.database import db_session
from msc.models import User
from msc.models import Customer
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

    # print('start add process...')
    name = request.form['inputName']
    # print("name is: " + name)
    password = request.form['inputPassword']
    # print("password is: " + password)
    password2 = request.form['inputPassword2']
    # print("password2 is: " + password2)
    user_company = request.form['inputCompanyName']
    # print("company: " + user_company)
    phone = request.form['inputPhone']
    # print("phone: " + phone)
    email = request.form['inputEmail']
    # print("email: " + email)
    streetAddress1 = request.form['inputStreetAddress1']
    # print("street address 1: " + streetAddress1)
    streetAddress2 = request.form['inputStreetAddress2']
    # print("street address 2: " + streetAddress2)
    city = request.form['inputCity']
    # print("city: " + city)
    state = request.form['inputState']
    # print("State: " + state)    
    country = request.form['inputCountry']
    # print("Country: " + country)
    postal = request.form['inputZip']
    # print("zip: " + postal)

    if not checkEmailAvailable(request):
        error = 'Sorry, that email is already taken'
        # print('email in use')
        return render_template('signup.html',  retUserName=name, retCompany=user_company, \
            retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, \
            retCity=city, retState=state, retZip=postal, retCountry=country, error=error)
    
    i = str(uuid.uuid4())

    session['userid'] = i
    
    # print('session ID in USER ADD--', session['userid'])

    if password == password2:
        updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        u = User(i, name, email, password, user_company, phone, streetAddress1, \
            streetAddress2, city, state, postal, country, updated_at)

        db_session.add(u)
        db_session.commit()

        flash('New user was successfully added')
        return redirect(url_for('home'))
    else:
        #print('unsuccessful add')
        error="passwords do not match"
        return render_template('signup.html', retUserName=name, retCompany=user_company, \
            retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, \
            retCity=city, retState=state, retZip=postal, retCountry=country, error=error)

    

@app.route('/view_user_request', methods=['GET'])
def view_user_request():

   # print("in view_user_request function - request method: " + request.method)
 
    the_user =  session['userid']
    result = User.query.filter(func.lower(User.id) == func.lower(the_user)).first()
    
    if result: 
        return render_template('customer_profile.html', fromProfile=True, retUserName=result.name, \
            retCompany=result.company, retEmail=result.email, retPhone=result.phone, retStreet1=result.address1, \
            retStreet2=result.address2, retCity=result.city, retState=result.state, retZip=result.postal, retCountry=result.country)
    else:
        return render_template('customer_profile.html', fromProfile=False)

       
@app.route('/view_user_request', methods=['post'])
def update_user_request():

   # print("in update_user_request function - request method: " + request.method)

    fromProfile = True

    name = request.form['inputName']
   # print("name is: " + name)
    user_company = request.form['inputCompanyName']
   # print("company: " + user_company)
    phone = request.form['inputPhone']
   # print("phone: " + phone)
    email = request.form['inputEmail']
   # print("email: " + email)   
    password = request.form['inputPassword']
   # print("password1: " + password)
    password2 = request.form['inputPassword2']
   # print("password2: " + password2)    
    streetAddress1 = request.form['inputStreetAddress1']
   # print("street address 1: " + streetAddress1)
    streetAddress2 = request.form['inputStreetAddress2']
   # print("street address 2: " + streetAddress2)
    city = request.form['inputCity']
   # print("city: " + city)
    state = request.form['inputState']
   # print("State: " + state)    
    country = request.form['inputCountry']
   # print("Country: " + country)
    postal = request.form['inputZip']
   # print("zip: " + postal)

    uid =  session['userid']
   # print('session ID in UPDATE--', session['userid'])

    updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    if len(password) != 0:
        if password != password2:
            error = 'passwords do not match'
            return render_template('customer_profile.html', fromProfile=fromProfile, retUserName=name, \
                retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, \
                retStreet2=streetAddress2, retCity=city, retState=state, retZip=postal, retCountry=country, \
                error=error)
        else:
            # update password
            hashedPassword = hashAPassword(getUser, password)
            result = User.query.filter(func.lower(User.id) == func.lower(uid)).first()
            if result:
                result.password = hashedPassword
                result.updated_at = updated_at
                db_session.update(result)
                db_session.commit()
            else:
                error = 'no user record found'
                return render_template('customer_profile.html', fromProfile=fromProfile, retUserName=name, \
                    retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, \
                    retStreet2=streetAddress2, retCity=city, retState=state, retZip=postal, retCountry=country, \
                    error=error)
    
    # update user record
    result = User.query.filter(func.lower(User.id) == func.lower(uid)).first()
    if result:
        result.name = name
        result.company = user_company
        result.email = email
        result.phone = phone
        result.address1 = streetAddress1
        result.address2 = streetAddress2
        result.city = city
        result.state = state
        result.postal = postal
        result.country = country
        result.updated_at = updated_at
        #db_session.update(result)
        db_session.commit()
    else:
        error = 'no user record found'
        return render_template('customer_profile.html', fromProfile=fromProfile, retUserName=name, \
            retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, \
            retStreet2=streetAddress2, retCity=city, retState=state, retZip=postal, retCountry=country, \
            error=error)


    flash('User was successfully updated')
    
    # print 'return from call:  ', user_profile.fetchone()  # or use fetchall()
   
    return render_template('customer_profile.html', fromProfile=fromProfile, retUserName=name, \
        retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, \
        retStreet2=streetAddress2, retCity=city, retState=state, retZip=postal, retCountry=country)


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
   # print("vendor: " + vendor)
    troubleshoot = ''
   # print("troubleshoot: " + troubleshoot)
    contact_name = request.form['inputContactName']
   # print("contact_name: " + contact_name)
    contact_phone = request.form['inputContactPhone']
   # print("contact_phone: " + contact_phone)
    contact_email = request.form['inputContactEmail']
   # print("contact_email: " + contact_email)
    manufacturer = request.form['inputEquipmentManufacturer']
   # print("manufacturer: " + manufacturer)
    model = request.form['inputEquipmentModel']
   # print("model: " + model)
    date_purchased = request.form['inputEquipmentDatePurchased']
   # print("date_purchased: " + date_purchased)
    appointment = request.form['inputTimeframe']
   # print("appointment: " + appointment)
    description = request.form['inputDescription']
   # print("description: " + description)

    i = str(uuid.uuid4())
    number = 3830238
    rtype = 'Service'
    status = 'Open'
    updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    provider = 'Advantage'


    #**** TODO SAVE RECORD

    flash('New request was successfully submitted')

    return True


def validUserRequest(request):
    # TODO
    return True

@app.route('/new_customer_request', methods=['GET'])
def new_customer_request():
    return render_template('new_customer.html')

def validCustomerAdd(request):
    # TODO
    return True

@app.route('/create_customer_request', methods=['POST'])
def create_customer_request():
    if not session.get('logged_in'):
        abort(401)

    error = None
    if not validCustomerAdd(request):
        error = 'Invalid data entered'
       # print('invalid data entered')
        return render_template('new_customer.html', error=error)

   # print('start add process...')
    customerID = request.form['inputCustomerID']
   # print("customerID is: " + customerID)
    customerName = request.form['inputCustomerName']
   # print("customer: " + customerName)
    customerType = request.form['inputCustomerType']
   # print("customer type: " + customerType)
    customerContact = request.form['inputCustomerContact']
   # print("contact: " + customerContact)
    phone1 = request.form['inputCustomerPhone1']
   # print("phone1: " + phone1)
    phone2 = request.form['inputCustomerPhone2']
   # print("phone2: " + phone2)
    fax = request.form['inputCustomerFax']
   # print("fax: " + fax)
    webAddy = request.form['inputCustomerWebsite']
   # print("website: " + webAddy)
    email = request.form['inputCustomerEmail']
   # print("email: " + email)
    streetAddress1 = request.form['inputCustomerAddress1']
   # print("street address 1: " + streetAddress1)
    streetAddress2 = request.form['inputCustomerAddress2']
   # print("street address 2: " + streetAddress2)
    city = request.form['inputCustomerCity']
   # print("city: " + city)
    state = request.form['inputCustomerState']
   # print("State: " + state)
    postal = request.form['inputCustomerZip']
   # print("zip: " + postal)
    country = request.form['inputCustomerCountry']
   # print("Country: " + country)
    streetAddress1Bill = request.form['inputCustomerBillAddress1']
   # print("street address 1: " + streetAddress1Bill)
    streetAddress2Bill = request.form['inputCustomerBillAddress2']
   # print("street address 2: " + streetAddress2Bill)
    cityBill = request.form['inputCustomerBillCity']
   # print("city: " + cityBill)
    stateBill = request.form['inputCustomerBillState']
   # print("State: " + stateBill)    
    postalBill = request.form['inputCustomerBillZip']
   # print("zip: " + postalBill)
    countryBill = request.form['inputCustomerBillCountry']
   # print("Country: " + countryBill)


#    May not be required for customer add
#    if not checkEmailAvailable(request):
#        error = 'Sorry, that email is already taken'
#        print('email in use')
#        return render_template('new_customer.html',  retUserName=name, retCompany=user_company, \
#            retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, \
#            retCity=city, retState=state, retZip=postal, retCountry=country, error=error)

    i = str(uuid.uuid4())
    updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    user_ID =  session['userid']

    c = Customer(i, user_ID, customerID, customerType, customerName, customerContact, email, \
        phone1, phone2, fax, webAddy, streetAddress1, streetAddress2, city, state, postal, country, \
        streetAddress1Bill, streetAddress2Bill, cityBill, stateBill, postalBill, countryBill, updated_at)

    db_session.add(c)
    db_session.commit()

    flash('New customer was successfully added')
    return redirect(url_for('home'))

#    This may end up in a database update try/catch 
#    else:
#        print('unsuccessful add')
#        error="failure adding new customer"
#        return render_template('new_customer.html', retUserName=name, retCompany=user_company, \
#            retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, \
#            retCity=city, retState=state, retZip=postal, retCountry=country, error=error)

@app.route('/list_customer_request', methods=['GET'])
def list_customer_request():    

   customers = Customer.query.all()

   for customer in customers:
    #print("customer " + customer.name)

   return render_template('customer_listing.html')

#    queryCustomers = db_session.query(Customer)
#    customeResult = queryCustomers.all()

#    if not customerResult:
#        return False
#    else: