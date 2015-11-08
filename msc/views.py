import uuid
from msc import app
from msc.database import db_session
from msc.models import User
from msc.models import Customer
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash
from sqlalchemy import func

import msc.view_service_request
import msc.view_user

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
    print("customer " + customer.name)

   return render_template('customer_listing.html')
