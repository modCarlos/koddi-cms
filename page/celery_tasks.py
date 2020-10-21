from celery import Celery
from django.core.mail import send_mail, send_mass_mail

app = Celery('celery_blog', broker='redis://localhost:6379/0')

"""
	Email Section
"""
@app.task
def send_email_with_celery(subject, message, to_mail):
	send_mail(subject, message, 'no-reply@koddi.com',[to_mail], fail_silently=False)

"""
	The main difference consist in that send_mass_mail works with only one open connection
"""

def send_mass_email_with_celery(messages):
	#Example of messages
	# message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
	#message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])

	send_mass_mail(messages, fail_silently=False)

"""
	Notifications Section - In progress
"""