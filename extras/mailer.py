from django.core.mail import send_mail
from django.contrib.auth.models import Group, User
from etcetera.settings import EMAIL_ADDRESS

def wo_mail(work_order):
	email_body = """A new work order (order ID %i) created by %s %s has been entered into Etcetera. Click here to view this ticket: http://etc.missouristate.edu/etcetera/service/%i.

Thank you!
- Etcetera""" % (work_order.id, work_order.first_name, work_order.last_name, work_order.id)
	email_subject = '[ETCETERA] New work order #%i' % work_order.id
	emails = []
	for user in User.objects.filter(groups__name="Equipment Service"):
		emails.append(user.email)
	send_mail(email_subject, email_body, EMAIL_ADDRESS, emails, fail_silently=False)
	
	email_subject = "We've received your work order for the %s" % (work_order.equipment_text,)
	email_body = """%s,
Your work order has been submitted successfully and our technicians have been notified.

You will be periodically notified via email if there's a change in status on your ticket. If at any other time you'd like to view your ticket, click here: http://etc.missouristate.edu/etcetera/service/%i.

Regards,

Educational Technology Center
Missouri State University""" % (work_order.first_name, work_order.id)
	send_mail(email_subject, email_body, EMAIL_ADDRESS, [work_order.email], fail_silently=False)