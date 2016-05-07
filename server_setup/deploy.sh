###############################################################################
# Assumptions:
# - CentOS 7
# - logged in as root
# - latest code checked out to /repo/msc
###############################################################################

#change configuration info for database
cd /repos/msc
sed -i -e 's/username/webapp/' msc/database.py
sed -i -e 's/password/ZfbX2yPcZ!W3P*wRk/' msc/database.py

#change configuration of wsgi
sed -i -e 's|pathToCode|/repos/msc|g' msc/msc.wsgi

cp msc/msc.wsgi /var/www/msc/
cp msc/msc.conf /etc/httpd/conf.d/

apachectl restart