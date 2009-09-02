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
from etcetera.extras.mailer import wo_mail, wo_mail_update, wo_mail_create
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
	query_string = ''
	paged_objects = None
	# If the request is a GET in any way (page number or query), then this
	# checks to see if there's a query being sent in GET and assigns it to a
	# variable to be sent to search middleware. If there's not a query in GET,
	# but there is a page number in GET, it pulls our query out of session
	# data. Otherwise, it makes sure to reset our session data for that
	# variable to None.
	#
	# Please note: the following may not be very Pythonic. I may be able to
	# rewrite this more efficiently someday.
	if request.GET:
		if 'q' in request.GET and request.GET['q'].strip():
			query_string = request.GET['q']
			request.session['q'] = query_string
		else:
			if 'q' in request.session:
				query_string = request.session['q']
	else:
		request.session['q'] = None
		query_string = None
	# This sends a query to search middleware, if such query exists. It gets
	# a Q object back which is used in a Django filter to get our queryset.
	if query_string:
		service_query = get_query(
			query_string, [
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
			]
		)
		# I'm keeping this longer than 80col because it's a Django filter.
		paged_objects = service.WorkOrder.objects.filter(service_query).filter(archived=archived).order_by('-creation_date')
	else:
		paged_objects = service.WorkOrder.objects.filter(archived=archived)
	
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
		'archived': archived,
		'q': query_string,
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
			if cd['complete']:
				if wo.completion_date:
					cd['completion_date'] = None;
				else:
					cd['completion_date'] = dt.datetime.now()
			else:
				cd['completion_date'] = wo.completion_date
			if cd['barcode']:
				cd['equipment'] = wo.barcode_lookup(cd['barcode'])
			else:
				cd['equipment'] = None
			form.save()
			wo_mail_update(wo)
			return HttpResponseRedirect(reverse(
				'etcetera.service.views.detail',
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
	return HttpResponseRedirect(reverse(
		'etcetera.service.views.detail',
		args=(wo.id,),
	))

@login_required
def new(request):
	if request.method == 'POST':
		form = woforms.WorkOrderModelForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			if cd['barcode']:
				cd['equipment'] = wo.barcode_lookup(cd['barcode'])
			else:
				cd['equipment'] = None
			wo = form.save()
			wo_mail_create(wo)
			return HttpResponseRedirect(reverse(
				'etcetera.service.views.detail',
				args=(wo.id,),
			))
	else:
		form = woforms.WorkOrderModelForm()
	context = {
		'form': form,
	}
	return render_to_response(
		"service/new.html",
		context,
		context_instance=RequestContext(request)
	)
