from msc import app
import uuid
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash
from msc.models import User
from sqlalchemy import func
from msc.database import db_session
from msc.send_email import send

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
    
    if password == password2:
        updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        u = User(i, name, email, password, user_company, phone, streetAddress1, \
            streetAddress2, city, state, postal, country, updated_at)

        db_session.add(u)
        db_session.commit()

        result = send(None, email, "Registration Confirmation", "Thanks for registering with MyServiceCompany.com")
        if(result != 1):
            #couldn't send email
            print("error when sending email: " + result)
        else:
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


def validUserRequest(request):
    # TODO
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

