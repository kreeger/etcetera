import os
import datetime as dt

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models as auth
from django.db.models import Avg, Sum, Count

from etcetera.settings import SITE_ROOT, DEBUG
from etcetera.extras.mailer import error_mail
from etcetera.extras import models as extras
from etcetera.extras import forms as exforms
from etcetera.service import models as service
from etcetera.checkout import models as checkout

def error_mail(request):
	# This sends an error mail. I'm not sure how this works but since I'm still
	# getting error emails from our server, I'm afraid to axe it.
	error_mail(request)
	return HttpResponseRedirect('etcetera-index')

def index(request):
	# This is some wonky fix for Python 2.5. Doesn't seem to affect Python 2.6,
	# so I'll be removing this when our server upgrades to Py2.6.
	if not DEBUG and not request.META['REQUEST_URI'].endswith('/'):
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
	# Get the user object of that user
	the_user = get_object_or_404(auth.User, username=the_user)
	# Try to get the user's profile object
	try:
		the_user.profile = the_user.get_profile()
	# If that profile doesn't exist, make the user create one
	except extras.UserProfile.DoesNotExist:
		# But only if the user is themselves
		if the_user == request.user:
			return HttpResponseRedirect(reverse('user-edit'))
		else:
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

def profile_related(request, the_user, view_type):
	if view_type not in ['workorders','checkouts',]: raise Http404
	# Get the user object of that user
	the_user = get_object_or_404(auth.User, username=the_user)
	if request.GET:
		# If form data is sent via GET (i.e., a set of dates coming in)
		form = exforms.DateSearchForm(request.GET)
		if form.is_valid():
			cd = form.cleaned_data
			if view_type == 'workorders':
				the_user.object_set = the_user.workorders.closed().filter(
					completion_date__range=(cd['start_date'], cd['end_date'])
				).order_by(
					'completion_date'
				)
			if view_type == 'checkouts':
				the_user.object_set = the_user.checkouts_delivered.filter(
					action_date__range=(cd['start_date'], cd['end_date'])
				).order_by(
					'action_date'
				)
	else:
		# Setup a few dates we'll be using
		week_ago = dt.datetime.today()+dt.timedelta(weeks=-1)
		thirty_days_ago = dt.datetime.today()+dt.timedelta(days=-30)
		form = exforms.DateSearchForm()
		if view_type == 'workorders':
			# Get the user's workorders based on time periods
			the_user.object_set = the_user.workorders.closed().filter(
				completion_date__gte=week_ago).order_by(
				'completion_date'
			)
		if view_type == 'checkouts':
			# Get the user's checkouts based on time periodsweek_ago
			the_user.object_set = the_user.checkouts_delivered.filter(
				action_date__gte=week_ago).order_by(
				'action_date'
			)
	# Do some totals and analysis
	if view_type == 'workorders':
		# Some analytic data on said workorders
		the_user.aggregates = the_user.object_set.aggregate(
			labor_sum=Sum('labor')
		)
	context = {
		'the_user': the_user,
		'view_type': view_type,
		'form': form,
	}
	if request.GET:
		context['start_date'] = form.cleaned_data['start_date']
		context['end_date'] = form.cleaned_data['end_date']
	return render_to_response(
		"extras/profile_related.html",
		context, 
		context_instance=RequestContext(request)
	)