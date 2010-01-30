import datetime as dt

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from etcetera.service import models as service
from etcetera.service import forms as woforms
from etcetera.equipment import models as equipment
from etcetera.service.mailer import *
from etcetera.extras.search import get_query

def service_form(request):
	# If data is being sent in POST, then get that data, clean it, and assign
	# it to a new WorkOrder instance.
	if request.method == 'POST':
		form = woforms.ServiceForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			wo = service.WorkOrder()
			name = cd['name'].split(' ')
			wo.first_name = name[0]
			wo.last_name = name[-1]
			wo.department_text = cd['department']
			wo.phone = cd['phone']
			wo.email = cd['email']
			wo.building = cd['building']
			wo.room = cd['room']
			wo.equipment_text = cd['equipment_text']
			if cd['barcode']:
				wo.equipment = wo.barcode_lookup(cd['barcode'])
			wo.description = cd['description']
			wo.work_type = cd['work_type']
			wo.save()
			created_mail(wo, cd['coordinator_check'])
			return HttpResponseRedirect('/thanks.html')
	# If data is not being sent in POST, our form is an empty one.
	else:
		form = woforms.ServiceForm()
	# Bundle our form in the context and send it out.
	context = {'form':form,}
	return render_to_response(
		"service/service_form.html",
		context, context_instance=RequestContext(request)
	)

@login_required
def index(request, view_type=None):
	paged_objects = None
	q = None
	form = woforms.SearchForm()
	if request.GET and request.GET.get('q'):
		form = woforms.SearchForm(request.GET)
		if form.is_valid():
			data = form.cleaned_data
			if data['q'] and data['q'].strip():
				# This sends a query to search middleware, if such
				# query exists. It gets a Q object back which is used
				# in a Django filter to get our queryset.
				service_query = get_query(data['q'], [
					'first_name',
					'last_name',
					'department_text',
					'department__name',
					'equipment__equipment_type__name',
					'equipment__make__name',
					'equipment__model',
					'equipment_text',
					'building__name',
					'room',
					'location_text',
					'description',
				])
				paged_objects = service.WorkOrder.objects.filter(
					service_query
				)
				q = data['q']
	else:
		paged_objects = service.WorkOrder.objects.all()
	if view_type == None:
		paged_objects = paged_objects.filter(
			completion_date=None).order_by(
			'-creation_date'
		)
	elif view_type == 'completed':
		paged_objects = paged_objects.exclude(
			completion_date=None).order_by(
			'-completion_date'
		)
	# Repackage everything into paged_objects using Paginator.
	paginator = Paginator(paged_objects, 20)
	# Make sure the page request is an int -- if not, then deliver page 1.
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	# If the page request is out of range, deliver the last page of results.
	try:
		paged_objects = paginator.page(page)
	except (EmptyPage, InvalidPage):
		paged_objects = paginator.page(paginator.num_pages)
	
	# Bundle everything into the context and send it out.
	context = {
		'paged_objects': paged_objects,
		'view_type': view_type,
		'form': form,
		'q': q,
	}
	return render_to_response(
		"service/index.html",
		context,
		context_instance=RequestContext(request)
	)

def detail(request, object_id):
	# Get the ticket from the URL, bundle it in a context, and send it out.
	wo = get_object_or_404(service.WorkOrder, id=object_id)
	context = {'object': wo,}
	return render_to_response(
		"service/detail.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def edit(request, object_id):
	# Get the workorder from the db	
	wo = get_object_or_404(service.WorkOrder, id=object_id)
	if request.method == 'POST':
		# Fill our form with the wo instance and post data
		form = woforms.WorkOrderModelForm(request.POST, instance=wo)
		if form.is_valid():
			cd = form.cleaned_data
			# If the work order is newly completed, send an email, if there is
			# an email specified in the form data
			if not wo.completed:
				if cd['completed']:
					if cd['email']:
						completed_mail(wo)
			# If there's a new barcode, look it up and add it
			# Future project: move to the model form
			# Brain hurts. Re-factor later
			if cd['barcode']:
				if wo.equipment:
					if cd['barcode'] != wo.equipment.barcode:
						try:
							cd['equipment'] = equipment.Equipment.objects.get(
								barcode=cd['barcode']
							)
						except equipment.Equipment.DoesNotExist:
							cd['equipment'] = None
				else:
					try:
						cd['equipment'] = equipment.Equipment.objects.get(
							barcode=cd['barcode']
						)
					except equipment.Equipment.DoesNotExist:
						cd['equipment'] = None
			else:
				cd['equipment'] = None
			form.save()
			if cd['completed']:
				return HttpResponseRedirect(reverse(
					'service-index',
				))
			return HttpResponseRedirect(reverse(
				'service-detail',
				args=(wo.id,),
			))
	else:
		initial_data = {}
		try:
			initial_data['barcode'] = equipment.Equipment.objects.get(pk=wo.equipment.id).barcode
		except (AttributeError):
			initial_data['barcode'] = None
		form = woforms.WorkOrderModelForm(instance=wo, initial=initial_data)
	context = {
		'object': wo,
		'form': form,
	}
	return render_to_response(
		"service/edit.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def pickup(request, object_id):
	# Get the ticket from the URL, bundle it in a context, and send it out.
	wo = get_object_or_404(service.WorkOrder, id=object_id)
	wo.technician = request.user
	wo.save()
	if wo.email:
		pickup_mail(wo)
	return HttpResponseRedirect(reverse(
		'service-detail',
		args=(wo.id,),
	))

@login_required
def new(request):
	if request.method == 'POST':
		form = woforms.WorkOrderModelForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			wo = service.WorkOrder()
			if cd['barcode']:
				cd['equipment'] = wo.barcode_lookup(cd['barcode'])
			else:
				cd['equipment'] = None
			wo = form.save()
			if wo.email:
				created_mail(wo)
			return HttpResponseRedirect(reverse(
				'service-detail',
				args=(wo.id,),
			))
	else:
		form = woforms.WorkOrderModelForm()
	context = {
		'form': form,
	}
	return render_to_response(
		"service/edit.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def cancel(request, object_id):
	# Get the object from the database
	wo = get_object_or_404(service.WorkOrder, id=object_id)
	# If page is accessed via POST
	if request.method == 'POST':
		# Check to see if the order has not yet been canceled
		if not wo.canceled and not wo.completion_date:
			# If not, set it as such and save it
			wo.canceled = True
			wo.completion_date = dt.datetime.now()
			wo.save()
			if wo.email:
				canceled_mail(wo)
			# Then trigger equipment as available
			#if wo.equipment:
			#	wo.equipment.status = 'installed'
			#	wo.equipment.save()
			# Then a redirect happens back to the submitting page
			return HttpResponseRedirect(reverse(
				'service-detail',
				args=(wo.id,),
			))
	# Otherwise create the context
	context = {
		'object': wo,
	}
	return render_to_response(
		"service/cancel.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def complete(request, object_id):
	wo = get_object_or_404(service.WorkOrder, id=object_id)
	now = dt.datetime.now()
	msg = None
	error = None
	# Maybe in the future I should move this into the save() method
	if not wo.completion_date:
		if wo.technician:
			# For  associated equipment item
			#if wo.equipment:
			#	# If it's marked as in repair
			#	if eq.status == 'repair':
			#		eq.status = 'installed'
			#		# Then mark as inventoried and save
			#		eq.last_inventoried = now
			#		eq.save()
			wo.completion_date = now
			wo.save()
			msg = u'Service order completed successfully. Patron has been notified.'
			if wo.email:
				completed_mail(wo)
		else:
			error = u'A technician needs to be assigned to this ticket before it can be completed.'
	# Redirect to detail
	context = {
		'object': wo,
		'error': error,
		'msg': msg,
	}
	return render_to_response(
		"service/detail.html",
		context,
		context_instance=RequestContext(request)
	)