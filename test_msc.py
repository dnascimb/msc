# -*- coding: utf-8 -*-
"""
    MSC Tests
    ~~~~~~~~~~~~

    Tests the MSC application.

    :copyright: (c) 2015 by Dan Nascimbeni.
"""

import pytest

import os
import msc
import tempfile


@pytest.fixture
def client(request):
    db_fd, msc.app.config['DATABASE'] = tempfile.mkstemp()
    msc.app.config['TESTING'] = True
    client = msc.app.test_client()
    with msc.app.app_context():
        msc.init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(msc.app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

def new_user_request(client):
    return client.get('/new_user_request', follow_redirects=True)

