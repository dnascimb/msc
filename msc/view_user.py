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

    name = request.form['inputName']
    password = request.form['inputPassword']
    password2 = request.form['inputPassword2']
    user_company = request.form['inputCompanyName']
    phone = request.form['inputPhone']
    email = request.form['inputEmail']
    streetAddress1 = request.form['inputStreetAddress1']
    streetAddress2 = request.form['inputStreetAddress2']
    city = request.form['inputCity']
    state = request.form['inputState']
    country = request.form['inputCountry']
    postal = request.form['inputZip']

    if not checkEmailAvailable(request):
        error = 'Sorry, that email is already taken'
        return render_template('signup.html',  retUserName=name, retCompany=user_company, \
            retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, \
            retCity=city, retState=state, retZip=postal, retCountry=country, error=error)
    
    i = str(uuid.uuid4())

    session['user_id'] = i
    
    if password == password2:
        u = User(i, name, email, password, user_company, phone, streetAddress1, \
            streetAddress2, city, state, postal, country)

        db_session.add(u)
        db_session.commit()

        result = send(None, email, "Registration Confirmation", "Thanks for registering with MyServiceCompany.com")
        if(result != 1):
            #couldn't send email
            print("error when sending email: " + result)
        else:
            session['logged_in'] = True
            return redirect(url_for('new_service_request'))
    else:
        #print('unsuccessful add')
        error="passwords do not match"
        return render_template('signup.html', retUserName=name, retCompany=user_company, \
            retEmail=email, retPhone=phone, retStreet1=streetAddress1, retStreet2=streetAddress2, \
            retCity=city, retState=state, retZip=postal, retCountry=country, error=error)

    

@app.route('/view_user_request', methods=['GET'])
def view_user_request():

    the_user =  session['user_id']
    result = User.query.filter(func.lower(User.id) == func.lower(the_user)).first()
    
    if result: 
        return render_template('customer_profile.html', fromProfile=True, retUserName=result.name, \
            retCompany=result.company, retEmail=result.email, retPhone=result.phone, retStreet1=result.address1, \
            retStreet2=result.address2, retCity=result.city, retState=result.state, retZip=result.postal, retCountry=result.country)
    else:
        return render_template('customer_profile.html', fromProfile=False)

       
@app.route('/view_user_request', methods=['post'])
def update_user_request():

    fromProfile = True

    name = request.form['inputName']
    user_company = request.form['inputCompanyName']
    phone = request.form['inputPhone']
    email = request.form['inputEmail']
    password = request.form['inputPassword']
    password2 = request.form['inputPassword2']
    streetAddress1 = request.form['inputStreetAddress1']
    streetAddress2 = request.form['inputStreetAddress2']
    city = request.form['inputCity']
    state = request.form['inputState']
    country = request.form['inputCountry']
    postal = request.form['inputZip']

    uid =  session['user_id']

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
                db_session.update(result)
                db_session.commit()
            else:
                error = 'no user record found'
                return render_template('customer_profile.html', fromProfile=fromProfile, retUserName=name, \
                    retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, \
                    retStreet2=streetAddress2, retCity=city, retState=state, retZip=postal, retCountry=country, \
                    error=error)
    
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
        db_session.update(result)
        db_session.commit()
    else:
        error = 'no user record found'
        return render_template('customer_profile.html', fromProfile=fromProfile, retUserName=name, \
            retCompany=user_company, retEmail=email, retPhone=phone, retStreet1=streetAddress1, \
            retStreet2=streetAddress2, retCity=city, retState=state, retZip=postal, retCountry=country, \
            error=error)


    flash('User was successfully updated')

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

