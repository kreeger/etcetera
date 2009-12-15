from django.core.mail import send_mail
from django.contrib.auth.models import Group, User
from etcetera.settings import EMAIL_ADDRESS

def created_mail(work_order, coordinator_check=True):
	body = "A new %s work order (#%i) for %s %s has been entered into Etcetera. Click here to view this ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\nName:\t\t%s %s\nDepartment:\t%s\nPhone:\t\t%s\nEmail:\t\t%s\nEquipment:\t%s\nLocation:\t%s %s\nDescription:\t%s\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nThanks!\n- Etcetera" % (
		work_order.work_type,
		work_order.id,
		work_order.first_name, work_order.last_name,
		work_order.id,
		work_order.first_name, work_order.last_name,
		work_order.department,
		work_order.phone,
		work_order.email,
		work_order.equipment_text,
		work_order.building, work_order.room,
		work_order.description,
	)
	subject = '[ETCETERA] New work order #%i' % work_order.id
	emails = []
	for user in User.objects.filter(groups__name="Equipment Service"):
		emails.append(user.email)
	send_mail(
		subject,
		body,
		EMAIL_ADDRESS,
		emails,
		fail_silently=False
	)
	if work_order.work_type == 'install' and not coordinator_check:
		body = "A new %s work order (#%i) for %s %s has been entered into Etcetera, which requires the attention of you, the classroom coordinator. Click here to view this ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\nName:\t%s %s\nDepartment:\t%s\nPhone:\t%s\nEmail:\t%s\nEquipment:\t%s\nLocation:\t%s %s\nDescription:\t%s\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nThanks!\n- Etcetera" % (
			work_order.work_type,
			work_order.id,
			work_order.first_name, work_order.last_name,
			work_order.id,
			work_order.first_name, work_order.last_name,
			work_order.department,
			work_order.phone,
			work_order.email,
			work_order.equipment_text,
			work_order.building, work_order.room,
			work_order.description,
		)
		send_mail(
			subject,
			body,
			EMAIL_ADDRESS,
			['davidcaravella@missouristate.edu'],
			fail_silently=False
		)
	patron_mail(work_order)

def patron_mail(work_order):
	subject = "A new work order (#%i) has been created for you" % (
		work_order.id,
	)
	body = "%s,\nYour new work order has been submitted successfully and our technicians have been notified.\n\nIf, at any time, you'd like to view your ticket, click here: http://etc.missouristate.edu/etcetera/service/%i.\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
		work_order.first_name,
		work_order.id
	)
	send_mail(
		subject,
		body,
		EMAIL_ADDRESS,
		[work_order.email],
		fail_silently=False
	)

def updated_mail(work_order):
	subject = "Your ETC service request (#%i) has been updated" % (
		work_order.id,
	)
	body = "%s,\nYour work order has been updated by a member of our service staff.\n\nVisit this link to view your updated ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
		work_order.first_name,
		work_order.id
	)
	send_mail(
		subject,
		body,
		EMAIL_ADDRESS,
		[work_order.email],
		fail_silently=False
	)

def completed_mail(work_order):
	subject = "Your work order (#%i) has been completed" % (
		work_order.id,
	)
	body = "%s,\nYour work order (#%i) has been completed.\n\nIf, at any time, you'd like to view your completed ticket, it is available here: http://etc.missouristate.edu/etcetera/service/%i.\n\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
		work_order.first_name,
		work_order.id,
		work_order.id
	)
	send_mail(
		subject,
		body,
		EMAIL_ADDRESS,
		[work_order.email],
		fail_silently=False
	)

def pickup_mail(work_order):
	subject = "Your work order (#%i) has been picked up" % (
		work_order.id,
	)
	body = "%s,\nYour work order has been picked up by %s %s, a member of our service staff.\n\nVisit this link to view your updated ticket: http://etc.missouristate.edu/etcetera/service/%i.\n\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
		work_order.first_name,
		work_order.technician.first_name, work_order.technician.last_name,
		work_order.id
	)
	send_mail(
		subject,
		body,
		EMAIL_ADDRESS,
		[work_order.email],
		fail_silently=False
	)
