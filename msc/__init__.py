# -*- coding: utf-8 -*-
"""
    MSC
    ~~~~~~

    An example service request application using Flask.

    :copyright: (c) 2015 by Dan Nascimbeni.

"""

from flask import Flask
from msc.database import db_session

# create the application
app = Flask(__name__)
app.secret_key = 'sipPinOnGinAndJuice'

import msc.views


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


