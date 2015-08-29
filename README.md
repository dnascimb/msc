# msc
Example project for creating service requests using Flask

Setup
=====

Project and Dependencies
------------------------

Mac

* $ git clone https://github.com/dnascimb/msc.git
* $ cd msc
* $ sudo pip install virtualenv
* $ virtualenv venv
* $ . venv/bin/activate
* $ pip install Flask (or for latest) pip install https://github.com/mitsuhiko/flask/tarball/master
* download and install sqlite


Application Initialization
--------------------------

* Change settings in msc.py
* $ flask --app=msc initdb


Start the Application
---------------------

* $ flask --app=msc run
* Open a browser to http://localhost:5000/
