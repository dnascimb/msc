import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = "admin@dannascimbeni.com"
receiver = "dnascimb@gmail.com"
subject = "Test Email From MyServiceCompany.com"
message = "do not try this at home"


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
    <p>Hello,<br>
       Thanks for signing up with MyServiceCompany.com!<br>
       Here is a link to Google, cause that's always helpful, <a href="http://www.google.com">google link</a> ...enjoy!
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

# Send the message via local SMTP server.
s = smtplib.SMTP('mail.privateemail.com', 26)
s.ehlo()
s.starttls()
s.login("admin@dannascimbeni.com","%FkdsuXc7FaD4")
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(sender, receiver, msg.as_string())
s.quit()
