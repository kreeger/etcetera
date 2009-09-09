from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models as auth

from etcetera.extras.mailer import error_mail
from etcetera.extras import models as extras
from etcetera.extras import forms as exforms

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

@login_required
def profile(request, the_user):
	if not the_user == request.user:
		the_user = get_object_or_404(auth.User, username=the_user)
	try:
		the_user.profile = the_user.get_profile()
	except extras.UserProfile.DoesNotExist:
		the_user.profile = None
	context = {
		'the_user': the_user,
	}
	return render_to_response(
		"extras/profile.html",
		context, 
		context_instance=RequestContext(request)
	)

@login_required
def change_password(request):
	user = request.user
	if request.method == 'POST':
		form = exforms.PasswordForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user.set_password(cd['password'])
			user.save()
			return HttpResponseRedirect(reverse(
				'etcetera-profile',
			))
	else:
		form = exforms.PasswordForm()
	context = {
		'user': user,
		'form': form,
	}
	return render_to_response(
		"extras/change-password.html",
		context, 
		context_instance=RequestContext(request)
	)