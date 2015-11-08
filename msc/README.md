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
* $ sudo pip install Flask (or for latest) pip install https://github.com/mitsuhiko/flask/tarball/master
* $ sudo pip install sqlalchemy
* $ sudo pip install PyMySQL
* download and install mysql
* adjust the database username and password in msc/database.py


Application Initialization
--------------------------

* $ python init_db.py
or
* $ flask --app=msc initdb


Start the Application (Development)
-----------------------------------

* $ python runserver.py
or
* $ flask --app=msc run
* Open a browser to http://localhost:5000/


Start the Application (Non-Development)
-----------------------------------

* edit **msc.wsgi** appropriately
* edit **msc.conf** appropriately
* make sure both apache and mod_wsgi are installed
* mv msc.wsgi /var/www/msc/
* mv msc.conf /etc/httpd/conf.d/
* apachectl restart
* Open a browser to http://yourhost.com
