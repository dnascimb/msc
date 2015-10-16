# -*- coding: utf-8 -*-
"""
    MSC
    ~~~~~~

    An example service request application using Flask.

    :copyright: (c) 2015 by Dan Nascimbeni.

"""

import uuid
from datetime import datetime
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash



# create the application
app = Flask(__name__)

import msc.views


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


