###############################################################################
# Assumptions:
# - CentOS 7
# - logged in as root
###############################################################################

#specify mysql repo and install
sudo yum -y update
sudo rpm -Uvh http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm
sudo yum install mysql-server -y
service mysql start

#provision mysql application user with limited permissions
mysql -u root -h0
CREATE DATABASE msc;
CREATE USER 'webapp'@'localhost' IDENTIFIED BY 'ZfbX2yPcZ!W3P*wRk';
GRANT SELECT, INSERT, UPDATE, DELETE, ALTER, CREATE, DROP, INDEX, LOCK TABLES, REFERENCES ON msc.* TO 'webapp'@'localhost';
exit

#install git
sudo yum install git -y
git config --global user.name "Dan Nascimbeni"
git config --global user.email "dnascimb@gmail.com"

#checkout msc project
mkdir /repos
sudo chmod 666 /repos
cd /repos
git clone https://github.com/dnascimb/msc.git
cd msc

#install apache
sudo yum install httpd -y
sudo systemctl start httpd.service

#install application pre-requisites
sudo yum install epel-release -y
sudo yum install python-pip -y
sudo yum install mod_wsgi -y
sudo yum install python34 -y
sudo pip install virtualenv
sudo pip install --upgrade virtualenv
virtualenv venv
. venv/bin/activate
#make python3 the active version for this environment
virtualenv -p python3 venv -y
sudo pip install https://github.com/mitsuhiko/flask/tarball/master
sudo pip install sqlalchemy
sudo pip install PyMySQL

#change configuration info for database
sed -i -e 's/username/webapp/' msc/database.py
sed -i -e 's/password/ZfbX2yPcZ!W3P*wRk/' msc/database.py

#change configuration of wsgi
sed -i -e 's|pathToCode|/repos/msc|g' msc/msc.wsgi

#copy code to apache
#cp -R ../msc /var/www
mkdir /var/www/msc
chown apache:apache -R /var/www/msc
cp msc/msc.wsgi /var/www/msc/
cp msc/msc.conf /etc/httpd/conf.d/
apachectl restart
