import smtplib
from email.mime.text import MIMEText


sender_email='sender_email@here.com'
receiver_email='recipient@example.com'
password='APP_PASSWORD_FROM_SMTP_PROVIDER'
subject =  'Email Subject Placed Here'
body = 'Hello, Email Body Placed Here'

# Creating Email Message
msg = MIMEText(body)
msg['Subject']=subject
msg['From']="Sender Name" # Default Sender Email
msg['To']=receiver_email


# Connect To SMTP Server And Semd Email
try:
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, msg.as_string())
		print("Email Sent Successfully")
except Exception as e:
	print(f'Error : {e}')

