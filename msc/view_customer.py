from msc import app
import uuid
from msc.database import db_session
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash
from msc.models import Customer

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

    c = Customer(i, user_ID, customerType, customerName, customerContact, email, \
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
