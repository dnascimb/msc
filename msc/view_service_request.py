from msc import app
import uuid
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash

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

