import os

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models as auth

from etcetera.settings import SITE_ROOT
from etcetera.extras.mailer import error_mail
from etcetera.extras import models as extras
from etcetera.extras import forms as exforms
from etcetera.service import models as service
from etcetera.checkout import models as checkout

# Don't quite know why I'm importing docutils. I should remove this.
#from docutils.core import publish_parts

def error_mail(request):
	# This sends an error mail. I'm not sure how this works but since I'm still
	# getting error emails from our server, I'm afraid to axe it.
	error_mail(request)
	return HttpResponseRedirect('etcetera-index')

def index(request):
	# This is some wonky fix for Python 2.5. Doesn't seem to affect Python 2.6,
	# so I'll be removing this when our server upgrades to Py2.6.
	if not request.META['REQUEST_URI'].endswith('/'):
		return HttpResponseRedirect("etcetera%s" % request.path)
	# Get the 5 most recent posts.
	posts = extras.Post.objects.all()[:5]
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
	# If the user profile being asked for isn't the current user,
	# get the user object of that user
	if not the_user == request.user:
		the_user = get_object_or_404(auth.User, username=the_user)
	# Try to get the user's profile object
	try:
		the_user.profile = the_user.get_profile()
	# If that profile doesn't exist, make the user create one
	except extras.UserProfile.DoesNotExist:
		# But only if the user is themselves
		if the_user == request.user:
			return HttpResponseRedirect(reverse('edit-profile'))
		else:
			the_user.profile = None
	# Get work order counts for user.
	workorders = service.WorkOrder.objects.filter(
		technician=the_user)
	the_user.workorders_closed = workorders.exclude(
		completion_date=None).count()
	the_user.workorders_open = workorders.filter(
		completion_date=None).count()
	# Get ticket counts.
	the_user.checkouts_handled = checkout.Checkout.objects.filter(
		handling_user=the_user).count()
	the_user.checkouts_delivered = checkout.Checkout.objects.filter(
		delivering_user=the_user).count()
	context = {
		'the_user': the_user,
	}
	return render_to_response(
		"extras/profile.html",
		context, 
		context_instance=RequestContext(request)
	)

@login_required
def edit_profile(request):
	# If a user is uploading data, try the following
	if request.method == 'POST':
		try:
			# This works when there's already a profile
			form = exforms.UserProfileForm(
				request.POST, request.FILES,
				instance=request.user.get_profile()
			)
		except extras.UserProfile.DoesNotExist:
			# If there's not a profile, create a new one with the data
			form = exforms.UserProfileForm(request.POST, request.FILES)
		if form.is_valid():
			# Validate it, save it, and get the object so
			# we can assign the user
			a_user = form.save()
			if not a_user.user:
				# If there's not already a user, make it the current user.
				a_user.user = request.user
				a_user.save()
			# Redirect to that user's page
			return HttpResponseRedirect(reverse(
				'etcetera-user',
				kwargs={'the_user': request.user},
			))
	# If there's not uploaded data, a new form should be drawn up
	else:
		try:
			# If there's already a profile, fill in the profile's data
			form = exforms.UserProfileForm(instance=request.user.get_profile())
		except extras.UserProfile.DoesNotExist:
			# Otherwise, it's a blank form!
			form = exforms.UserProfileForm()
		except AttributeError:
			# Had to add this to handle some Attribute Errors that popped up
			return HttpResponseRedirect(reverse('etcetera-login'))
	context = {
		'the_user': request.user,
		'form': form,
	}
	return render_to_response(
		"extras/edit-profile.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def change_password(request):
	# First we get our current user
	user = request.user
	if request.method == 'POST':
		# If data is submitted, get that password change form and fill it
		form = exforms.PasswordForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			# If all is valid, set the password and save the user
			user.set_password(cd['password'])
			user.save()
			return HttpResponseRedirect(reverse(
				'etcetera-user',
				kwargs={'the_user': request.user},
			))
	# If not in POST, send an empty form
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
