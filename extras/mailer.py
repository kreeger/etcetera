from django.core.mail import send_mail
from django.contrib.auth.models import Group, User
from etcetera.settings import EMAIL_ADDRESS

def wo_mail(work_order):
	email_body = "A new work order (#%i) created by %s %s has been entered into Etcetera. Click here to view this ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\nThanks!\n- Etcetera" % (
		work_order.id,
		work_order.first_name,
		work_order.last_name,
		work_order.id
	)
	email_subject = '[ETCETERA] New work order #%i' % work_order.id
	emails = []
	for user in User.objects.filter(groups__name="Equipment Service"):
		emails.append(user.email)
	send_mail(
		email_subject,
		email_body,
		EMAIL_ADDRESS,
		emails,
		fail_silently=False
	)
	
	email_subject = "We've received your work order (#%i) for the %s" % (
		work_order.id, work_order.equipment_text,
	)
	email_body = "%s,\nYour work order has been submitted successfully and our technicians have been notified.\n\nYou will be periodically notified via email if there's a change in status on your ticket. If at any other time you'd like to view your ticket, click here: http://etc.missouristate.edu/etcetera/service/%i.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
		work_order.first_name,
		work_order.id
	)
	send_mail(
		email_subject,
		email_body,
		EMAIL_ADDRESS,
		[work_order.email],
		fail_silently=False
	)

def wo_mail_update(work_order):
	email_subject = "Your ETC service request (#%i) has been updated" % (
		work_order.id,
	)
	email_body = "%s,\nYour work order has been updated by a member of our service staff.\n\nVisit this link to view your updated ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
		work_order.first_name,
		work_order.id
	)
	send_mail(
		email_subject,
		email_body,
		EMAIL_ADDRESS,
		[work_order.email],
		fail_silently=False
	)

def error_mail(request):
	email_body = "There's been an error.\n\nPath:\t%s\nMethod:\t%s\nUser:\t%s\nHost:\t%s\n\nRequest dictionary:\n" % (
		request.build_absolute_uri(),
		request.method,
		request.user,
		request.get_host()
	)
	for key in request.META:
		email_body += "%s:\t%s\n" % (key, request.META[key])
	email_body += "\nSession data:\n"
	for key in request.session:
		email_body += "%s:\t%s\n" % (key, request.session[key])
	emails = []
	for user in User.objects.filter(groups__name="System Administrators"):
		emails.append(user.email)
	send_mail(
		'[ETCETERA] Error at %s' % (request.build_absolute_uri(),),
		email_body,
		EMAIL_ADDRESS,
		emails,
		fail_silently=False
	)
