# server_setup
Instructions for setting up a production application server for this application

Machine Creation
------------------------

DigitalOcean - CentOS 7.2

* create machine
* load machine with SSH key (follow instructions for that on the web - or use admin GUI)
* get setup.sh to the machine via scp
* SSH into the machine as root
* run the setup.sh script
* go to http://machine:80 and check for the login screen
* if issues check console or /var/log/httpd/error_log



Deploy Latest
------------------------

Frequently, the latest code will need to be deployed. In absense of a build server, deploy.sh can be run immediately after the latest code has been checked out on the machine to "/repos/msc".