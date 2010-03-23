from django.core.mail import send_mail
from django.contrib.auth.models import Group, User
from etcetera.settings import EMAIL_ADDRESS

def created_mail(checkout):
    body = "A new equipment checkout (#%i) for %s %s has been entered into Etcetera. Click here to view this ticket: http://etc.missouristate.edu/etcetera/checkout/%i.\n\nType:\t\t%s / %s returns\nName:\t\t%s %s\nDepartment:\t%s\nPhone:\t\t%s\nEmail:\t\t%s\nLocation:\t%s %s\nEquipment:\t%s\nFrom:\t\t%s\nUntil:\t\t%s\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nThanks!\n- Etcetera" % (
        checkout.id,
        checkout.first_name, checkout.last_name,
        checkout.id,
        checkout.checkout_type, checkout.return_type,
        checkout.first_name, checkout.last_name,
        checkout.department_text,
        checkout.phone,
        checkout.email,
        checkout.building, checkout.room,
        checkout.equipment_needed,
        checkout.out_date,
        checkout.return_date,
    )
    subject = '[ETCETERA] New equipment checkout #%i' % checkout.id
    emails = []
    for user in User.objects.filter(groups__name="Equipment Lending"):
        emails.append(user.email)
    send_mail(
        subject,
        body,
        EMAIL_ADDRESS,
        emails,
        fail_silently=False
    )
    patron_mail(checkout)

def patron_mail(checkout):
    subject = "A new equipment checkout (#%i) has been created for you" % (
        checkout.id,
    )
    body = "%s,\nYour new equpiment checkout has been submitted successfully and our technicians have been notified.\n\nIf, at any time, you'd like to view your ticket, click here: http://etc.missouristate.edu/etcetera/checkout/%i.\n\nNote that this message does not confirm that your equipment is available for the date and time you've specified; you will receive another email once everything has been confirmed. Otherwise you will be contacted to schedule another date and time (or alternate equipment).\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
        checkout.first_name,
        checkout.id
    )
    send_mail(
        subject,
        body,
        EMAIL_ADDRESS,
        [checkout.email],
        fail_silently=False
    )

def updated_mail(checkout):
    subject = "Your ETC equipment checkout (#%i) has been updated" % (
        checkout.id,
    )
    body = "%s,\nYour equipment checkout has been updated by a member of our service staff.\n\nVisit this link to view your updated ticket: http://etc.missouristate.edu/etcetera/checkout/%i.\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
        checkout.first_name,
        checkout.id
    )
    send_mail(
        subject,
        body,
        EMAIL_ADDRESS,
        [checkout.email],
        fail_silently=False
    )

def completed_mail(checkout):
    subject = "Your ETC equipment checkout (#%i) has been closed" % (
        checkout.id,
    )
    body = "%s,\nYour equipment checkout (#%i) has been completed.\n\nIf, at any time, you'd like to view your completed checkout, it is available here: http://etc.missouristate.edu/etcetera/checkout/%i.\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
        checkout.first_name,
        checkout.id,
        checkout.id
    )
    send_mail(
        subject,
        body,
        EMAIL_ADDRESS,
        [checkout.email],
        fail_silently=False
    )
    
def confirmation_mail(checkout):
    subject = "ETC Equipment Checkout Confirmation (Ticket #%i)" % (
        checkout.id,
    )
    body = "%s,\nCongratulations! We have just confirmed your equipment checkout request (ticket #%i). Your equipment will be ready for %s at the date and time shown below.\n\nEquipment:\t%s\nFrom:\t\t%s\nUntil:\t\t%s\n\n" % (
        checkout.first_name,
        checkout.id,
        checkout.checkout_type,
        checkout.equipment_needed,
        checkout.out_date,
        checkout.return_date,
    )
    if checkout.return_type == 'requestor':
        body += "Remember that your equipment is due back on time. If you do not bring the equipment back by the time shown above, late fees will be assessed. Please remember to keep the equipment secure when not in use.\n\n"
    
    body += "If, at any time, you'd like to view your ticket, click here: http://etc.missouristate.edu/etcetera/checkout/%i.\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
        checkout.id,
    )
    send_mail(
        subject,
        body,
        EMAIL_ADDRESS,
        [checkout.email],
        fail_silently=False
    )

def delivery_assignment_mail(checkout, delivering_user):
    subject = "An equipment checkout (#%i) has been given to you for delivery" % (
        checkout.id,
    )
    body = "%s,\nAn equipment checkout ticket (#%i) has been given to you for delivery. You may view this ticket here: http://etc.missouristate.edu/etcetera/checkout/%i.\n\nIt will also show up in your list of tickets for delivery. To view these once you're logged into Etcetera, click your name in the upper-right-hand corner of the page.\n\n-------------\nPlease do not reply to this message, as nobody will receive it.\n\nRegards,\nEducational Technology Center\nMissouri State University" % (
        delivering_user.first_name,
        checkout.id,
        checkout.id,
    )
    send_mail(
        subject,
        body,
        EMAIL_ADDRESS,
        [delivering_user.email],
        fail_silently=False
    )

def canceled_mail(checkout, reason):
    subject = "Your ETC equipment checkout (#%i) has been canceled" % (
        checkout.id,
    )
    body = """%s,\nYour equipment checkout (#%i) has been canceled. The reason for cancellation is stated below:\n\n"%s"\n\nIf, at any time, you'd like to view your canceled checkout, it is available here: http://etc.missouristate.edu/etcetera/checkout/%i.\n\n-------------\nPlease do not reply to this message, as nobody will receive it. If your checkout has been canceled in error, please contact Rebecca Grant at rebeccagrant@missouristate.edu.\n\nRegards,\nEducational Technology Center\nMissouri State University""" % (
        checkout.first_name,
        checkout.id,
        reason,
        checkout.id
    )
    send_mail(
        subject,
        body,
        EMAIL_ADDRESS,
        [checkout.email],
        fail_silently=False
    )