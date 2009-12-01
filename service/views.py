import datetime as dt

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from etcetera.service import models as service
from etcetera.service import forms as woforms
from etcetera.equipment import models as equipment
from etcetera.extras.mailer import wo_mail, wo_mail_complete, wo_mail_pickup, wo_mail_create
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
			wo.department = cd['department']
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
			wo_mail(wo, cd['coordinator_check'])
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
def index(request, archived=False):
	paged_objects = None
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
					'department',
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
				).filter(
					archived=archived
				)
			else:
				paged_objects = service.WorkOrder.objects.filter(
					archived=archived
				)
	else:
		paged_objects = service.WorkOrder.objects.filter(
			archived=archived
		)
	if archived:
		paged_objects = paged_objects.order_by('-completion_date')
	else:
		paged_objects = paged_objects.order_by('-creation_date')
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
		'form': form,
		'archived': archived,
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
	wo = get_object_or_404(service.WorkOrder, id=object_id)
	if request.method == 'POST':
		form = woforms.WorkOrderModelForm(request.POST, instance=wo)
		if form.is_valid():
			cd = form.cleaned_data
			# I should eventually move this into forms.WorkOrderModelForm
			if cd['archived']:
				cd['completion_date'] = dt.datetime.now()
				if cd['email']:
					wo_mail_complete(wo)
			else:
				cd['completion_date'] = wo.completion_date
			if cd['uncomplete']:
				cd['completion_date'] = None;
			if cd['barcode']:
				cd['equipment'] = wo.barcode_lookup(cd['barcode'])
			else:
				cd['equipment'] = None
			form.save()
			if cd['archived']:
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
	wo_mail_pickup(wo)
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
			wo_mail_create(wo)
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
