from django.core.mail import send_mail
from django.contrib.auth.models import Group, User
from etcetera.settings import EMAIL_ADDRESS

def wo_mail(work_order, coordinator_check):
	email_body = "A new %s work order (#%i) created by %s %s has been entered into Etcetera. Click here to view this ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\nName:\t%s %s\nDepartment:\t%s\nPhone:\t%s\nEmail:\t%s\nLocation:\t%s %s\nDescription:\t%s\n\nPlease do not reply to this message, as nobody will receive it.\n\nThanks!\n- Etcetera" % (
		work_order.work_type,
		work_order.id,
		work_order.first_name,
		work_order.last_name,
		work_order.id,
		work_order.first_name,
		work_order.last_name,
		work_order.department,
		work_order.phone,
		work_order.email,
		work_order.building,
		work_order.room,
		work_order.description,
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
	if work_order.work_type == 'install' and not coordinator_check:
		email_body = "A new %s work order (#%i) created by %s %s has been entered into Etcetera, which requires the attention of you, the classroom coordinator. Click here to view this ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\nName:\t%s %s\nDepartment:\t%s\nPhone:\t%s\nEmail:\t%s\nEquipment:\t%s\nLocation:\t%s %s\nDescription:\t%s\n\nPlease do not reply to this message, as nobody will receive it.\n\nThanks!\n- Etcetera" % (
			work_order.work_type,
			work_order.id,
			work_order.first_name,
			work_order.last_name,
			work_order.id,
			work_order.first_name,
			work_order.last_name,
			work_order.department,
			work_order.phone,
			work_order.email,
			work_order.equipment_text,
			work_order.building,
			work_order.room,
			work_order.description,
		)
		send_mail(
			email_subject,
			email_body,
			EMAIL_ADDRESS,
			['davidcaravella@missouristate.edu'],
			fail_silently=False
		)
	wo_mail_create(work_order)

def wo_mail_create(work_order):
	email_subject = "A new work order (#%i) has been created for you" % (
		work_order.id,
	)
	email_body = "%s,\nYour new work order has been submitted successfully and our technicians have been notified.\n\nIf, at any time, you'd like to view your ticket, click here: http://etc.missouristate.edu/etcetera/service/%i.\n\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
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
	email_body = "%s,\nYour work order has been updated by a member of our service staff.\n\nVisit this link to view your updated ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
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

def wo_mail_complete(work_order):
	email_subject = "Your work order (#%i) has been completed" % (
		work_order.id,
	)
	email_body = "%s,\nYour work order (#%i) has been completed.\n\nIf, at any time, you'd like to view your completed ticket, it is available here: http://etc.missouristate.edu/etcetera/service/%i.\n\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
		work_order.first_name,
		work_order.id,
		work_order.id
	)
	send_mail(
		email_subject,
		email_body,
		EMAIL_ADDRESS,
		[work_order.email],
		fail_silently=False
	)

def wo_mail_pickup(work_order):
	email_subject = "Your work order (#%i) has been picked up" % (
		work_order.id,
	)
	email_body = "%s,\nYour work order has been picked up by %s %s, a member of our service staff.\n\nVisit this link to view your updated ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
		work_order.first_name,
		work_order.technician.first_name,
		work_order.technician.last_name,
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
