from django.http import HttpResponseRedirect
from etcetera.extras.mailer import error_mail

def error_mail(request):
	error_mail(request)
	return HttpResponseRedirect('/etcetera/')
