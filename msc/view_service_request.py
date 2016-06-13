from msc import app
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash
from msc.models import Ticket, TicketType, TicketSchema, TicketStatus, TimeSlot, User
from msc.database import db_session
import uuid
import json
import pprint

@app.route('/new_service_request', methods=['GET'])
def new_service_request():
    if not session.get('logged_in'):
        abort(401)
    ticket_types = TicketType.query.all()
    time_slots = TimeSlot.query.all()
    return render_template('new_service_request.html', ticket_types=ticket_types, time_slots=time_slots)


@app.route('/tickets', methods=['POST'])
def create_service_request():
    if not session.get('logged_in'):
        abort(401)

    error = None
    if not validServiceRequest(request):
        error = 'Invalid data entered'
        return render_template('new_service_request.html', error=error)

    result = saveRequest(request)
    if(result is None):
        abort(500)
    else:
        return json.dumps({'id': result.id }), 201

@app.route('/home', methods=['GET'])
def home():
    if not session.get('logged_in'):
        abort(401)

    #results = Ticket.query.filter_by(reporter=session.get('user_id')).all()
    results = Ticket.query.all()
    ticket_types = TicketType.query.all()
    ticket_statuses = TicketStatus.query.all()
#   RETURN JSON
    #str_result = ""
    # for result in results:
    #     ticket_schema = TicketSchema()
    #     str_result+=ticket_schema.dumps(result).data
    # return str_result, 200
    return render_template('service_request_listing.html', tickets=results, ticket_types=ticket_types, \
        ticket_statuses=ticket_statuses)

@app.route('/user/<uid>/tickets/<ticket_id>', methods=['GET'])
def view_user_ticket(uid=None, ticket_id=None):
    if not session.get('logged_in') or not uid or not ticket_id:
        abort(401)

    result = Ticket.query.filter_by(id=ticket_id).first()
    if not result:
        return(404) #no ticket
    ticket_types = TicketType.query.all()
    ticket_statuses = TicketStatus.query.all()
    time_slots = TimeSlot.query.all()
    reporter = User.query.filter_by(id=result.reporter).first()
    current_user = User.query.filter_by(id=session.get('user_id')).first()
#   RETURN JSON
    #str_result = ""
    # for result in results:
    #     ticket_schema = TicketSchema()
    #     str_result+=ticket_schema.dumps(result).data
    # return str_result, 200
    return render_template('service_request.html', ticket=result, ticket_types=ticket_types, \
        ticket_statuses=ticket_statuses, time_slots=time_slots, reporter=reporter, current_user=current_user)

@app.route('/user/<uid>/tickets/<ticket_id>', methods=['PUT'])
def confirm_appointment_request(uid=None, ticket_id=None):
    if not session.get('logged_in'):
        abort(401)

    error = None
    if not validServiceRequest(request):
        error = 'Invalid data entered'
        return render_template('new_service_request.html', error=error)

    #get data to update
    jdata = json.loads(request.get_data().decode('utf-8'))
    new_appointment_date = jdata['appointment_date']
    new_appointment_timeslot = jdata['appointment_timeslot']

    ticket = Ticket.query.filter_by(id=ticket_id).first()
    
    if(ticket is None):
        abort(500)
    else:
        ticket.appointment_confirmed = True
        ticket.status += 1 #how to increment status better?
        ticket.appointment_at = new_appointment_date
        ticket.timeslot = new_appointment_timeslot

        db_session.commit() #save new data

        ticket = Ticket.query.filter_by(id=ticket_id).first()

        result = "{ \"id\": \"" + ticket.id + "\", "
        result += " \"reporter\": \"" + ticket.reporter + "\", "
        result += " \"provider\": \"" + ticket.provider + "\", "
        result += " \"type\": \"" + str(ticket.type) + "\", "
        result += " \"status\": \"" + str(ticket.status) + "\", "
        result += " \"quantity\": \"" + str(ticket.quantity) + "\", "
        result += " \"pm_contract\": \"" + str(ticket.pm_contract) + "\", "
        result += " \"description\": \"" + str(ticket.description) + "\", "
        result += " \"timeslot\": \"" + str(ticket.timeslot) + "\", "
        result += " \"appointment_at\": \"" + str(ticket.appointment_at) + "\", "
        result += " \"appointment_confirmed\": \"" + str(ticket.appointment_confirmed) + "\", "
        result += " \"created_at\": \"" + str(ticket.created_at) + "\", "
        result += " \"updated_at\": \"" + str(ticket.updated_at) + "\" }"
        return json.dumps(result), 200


@app.route('/user/<uid>/tickets/<ticket_id>', methods=['PATCH'])
def change_status(uid=None, ticket_id=None):
    if not session.get('logged_in'):
        abort(401)

    error = None
    if not validServiceRequest(request):
        error = 'Invalid data entered'
        return render_template('service_request.html', error=error)

    #get data to update
    jdata = json.loads(request.get_data().decode('utf-8'))
    print(repr(jdata))
    new_status = jdata['status']

    ticket = Ticket.query.filter_by(id=ticket_id).first()
    
    if(ticket is None):
        abort(500)
    else:
        ticket.status = new_status
        db_session.commit() #save new data
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        result = "{ \"id\": \"" + ticket.id + "\", "
        result += " \"reporter\": \"" + ticket.reporter + "\", "
        result += " \"provider\": \"" + ticket.provider + "\", "
        result += " \"type\": \"" + str(ticket.type) + "\", "
        result += " \"status\": \"" + str(ticket.status) + "\", "
        result += " \"quantity\": \"" + str(ticket.quantity) + "\", "
        result += " \"pm_contract\": \"" + str(ticket.pm_contract) + "\", "
        result += " \"description\": \"" + str(ticket.description) + "\", "
        result += " \"timeslot\": \"" + str(ticket.timeslot) + "\", "
        result += " \"appointment_at\": \"" + str(ticket.appointment_at) + "\", "
        result += " \"appointment_confirmed\": \"" + str(ticket.appointment_confirmed) + "\", "
        result += " \"created_at\": \"" + str(ticket.created_at) + "\", "
        result += " \"updated_at\": \"" + str(ticket.updated_at) + "\" }"
        return json.dumps(result), 200


def validServiceRequest(request):
    # TODO
    return True

def saveRequest(request):
    ticket = request.get_data().decode('utf-8')
    reporter = session.get('user_id')
    
    if not reporter:
        return None
    
    if not (ticket is None):
        i = str(uuid.uuid4())
        jticket = json.loads(ticket)
        t = Ticket(i, reporter, jticket['type'], jticket['quantity'], jticket['pm'], jticket['desc'], \
        jticket['timeframe'], jticket['date_requested'], 1)

        db_session.add(t)
        db_session.commit()

    return t

