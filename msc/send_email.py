import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(sender,receiver,subject,message):

	if not sender:
		sender = "MyServiceCompany.com <admin@dannascimbeni.com>"
	if not receiver:
		return "no receiver specified"
	if not subject:
		return "no subject specified"
	if not message:
		return "no message specified"


	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = receiver

	# Create the body of the message (a plain-text and an HTML version).
	text = message
	html = """\
	<html>
	  <head></head>
	  <body>
	    <p>Hello,<br><br>
       Thanks for signing up with <a href="http://www.myservicecompany.com">MyServiceCompany.com</a><br>
    </p>
	  </body>
	</html>
	"""

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via SMTP server.
	s = smtplib.SMTP('mail.privateemail.com', 26)
	s.ehlo()
	s.starttls()
	s.login("admin@dannascimbeni.com","%FkdsuXc7FaD4")
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(sender, receiver, msg.as_string())
	s.quit()
	return 1