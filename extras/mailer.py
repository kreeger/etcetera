from django.core.mail import send_mail
from django.contrib.auth.models import Group, User
from etcetera.settings import EMAIL_ADDRESS

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
