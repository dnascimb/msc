from msc import app
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash
from msc.models import Ticket, TicketType, TicketSchema, TicketStatus
from msc.database import db_session
import uuid
import json
import pprint

@app.route('/new_service_request', methods=['GET'])
def new_service_request():
    if not session.get('logged_in'):
        abort(401)
    ticket_types = TicketType.query.all()
    return render_template('new_service_request.html', ticket_types=ticket_types)


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
#   RETURN JSON
    #str_result = ""
    # for result in results:
    #     ticket_schema = TicketSchema()
    #     str_result+=ticket_schema.dumps(result).data
    # return str_result, 200
    return render_template('service_request.html', ticket=result, ticket_types=ticket_types, \
        ticket_statuses=ticket_statuses)


def validServiceRequest(request):
    # TODO
    return True

def saveRequest(request):
    ticket = request.get_data().decode('utf-8');
    reporter = session.get('user_id')
    
    if not reporter:
        return None
    
    if not (ticket is None):
        i = str(uuid.uuid4())
        jticket = json.loads(ticket);
        t = Ticket(i, reporter, jticket['type'], jticket['quantity'], jticket['pm'], jticket['desc'], \
        jticket['timeframe'], jticket['date_requested'], 1)

        db_session.add(t)
        db_session.commit()

    return t;

