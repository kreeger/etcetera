from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from etcetera.extras.mailer import error_mail
from etcetera.extras import models as extras

from docutils.core import publish_parts

def error_mail(request):
	error_mail(request)
	return HttpResponseRedirect('/etcetera/')

def index(request):
	posts = extras.Post.objects.all()
	context = {
		'object_list': posts,
	}
	return render_to_response(
		"index.html",
		context, 
		context_instance=RequestContext(request)
	)
