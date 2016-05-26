from msc import app
from datetime import datetime
from flask import request, session, redirect, url_for, abort, \
     render_template, flash
from msc.models import Ticket
from msc.database import db_session
import uuid
import json

@app.route('/new_service_request', methods=['GET'])
def new_service_request():
    if not session.get('logged_in'):
        abort(401)
    return render_template('new_service_request.html')


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
        updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        jticket = json.loads(ticket);
        t = Ticket(i, reporter, jticket['type'], jticket['quantity'], jticket['pm'], jticket['desc'], \
        jticket['timeframe'], jticket['date_requested'], updated_at)

        db_session.add(t)
        db_session.commit()

    return t;

