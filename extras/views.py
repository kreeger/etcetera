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

from docutils.core import publish_parts
from git import *

def error_mail(request):
	error_mail(request)
	return HttpResponseRedirect('etcetera-index')

def index(request):
	# Hack to put the trailing slash on the root
	if not request.META['REQUEST_URI'].endswith('/'):
		# This is bad and I should most likely NOT hardcode this
		return HttpResponseRedirect("etcetera%s" % request.path)
	#repo = Repo(SITE_ROOT)
	#commits = repo.commits('master', max_count=3)
	posts = extras.Post.objects.all()[:3]
	context = {
		'object_list': posts,
	#	'commits': commits,
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
		if the_user == request.user:
			return HttpResponseRedirect(reverse('edit-profile'))
		else:
			the_user.profile = None
	# Get work order counts for user.
	workorders = service.WorkOrder.objects.filter(
		technician=the_user)
	the_user.workorders_closed = workorders.filter(completed=True).count()
	the_user.workorders_open = workorders.filter(completed=False).count()
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

def edit_profile(request):
	if request.method == 'POST':
		try:
			form = exforms.UserProfileForm(
				request.POST, request.FILES,
				instance=request.user.get_profile()
			)
		except extras.UserProfile.DoesNotExist:
			form = exforms.UserProfileForm(request.POST, request.FILES)
		if form.is_valid():
			if not form.cleaned_data['user']:
				form.cleaned_data['user'] = request.user
			form.save()
			return HttpResponseRedirect(reverse(
				'etcetera-user',
				kwargs={'the_user': request.user},
			))
	else:
		try:
			form = exforms.UserProfileForm(instance=request.user.get_profile())
		except extras.UserProfile.DoesNotExist:
			form = exforms.UserProfileForm()
		except AttributeError:
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
	user = request.user
	if request.method == 'POST':
		form = exforms.PasswordForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user.set_password(cd['password'])
			user.save()
			return HttpResponseRedirect(reverse(
				'etcetera-user',
				kwargs={'the_user': request.user},
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
