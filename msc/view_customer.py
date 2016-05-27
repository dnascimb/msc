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
        return render_template('new_customer.html', error=error)

    companyName = request.form['inputCompanyName']
    customerType = request.form['inputCustomerType']
    customerLastName = request.form['inputCustomerLastName']
    customerFirstName = request.form['inputCustomerFirstName']
    phone1 = request.form['inputCustomerPhone1']
    phone2 = request.form['inputCustomerPhone2']
    fax = request.form['inputCustomerFax']
    webAddy = request.form['inputCustomerWebsite']
    email = request.form['inputCustomerEmail']
    streetAddress1 = request.form['inputCustomerAddress1']
    streetAddress2 = request.form['inputCustomerAddress2']
    city = request.form['inputCustomerCity']
    state = request.form['inputCustomerState']
    postal = request.form['inputCustomerZip']
    country = request.form['inputCustomerCountry']
    streetAddress1Bill = request.form['inputCustomerBillAddress1']
    streetAddress2Bill = request.form['inputCustomerBillAddress2']
    cityBill = request.form['inputCustomerBillCity']
    stateBill = request.form['inputCustomerBillState']
    postalBill = request.form['inputCustomerBillZip']
    countryBill = request.form['inputCustomerBillCountry']

    i = str(uuid.uuid4())
    user_ID =  session['user_id']

    c = Customer(i, user_ID, customerType, companyName, customerLastName, customerFirstName, email, \
        phone1, phone2, fax, webAddy, streetAddress1, streetAddress2, city, state, postal, country, \
        streetAddress1Bill, streetAddress2Bill, cityBill, stateBill, postalBill, countryBill)

    db_session.add(c)
    db_session.commit()

    flash('New customer was successfully added')
    return redirect(url_for('home'))


@app.route('/list_customer_request', methods=['GET'])
def list_customer_request():    

   customers = Customer.query.all()

   for customer in customers:
    print("customer company:  " + customer.company_name)
    print("customer last name:  " + customer.contact_last_name)

   return render_template('customer_listing.html', retCustomers=customers)
