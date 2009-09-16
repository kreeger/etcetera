import datetime as dt

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from etcetera.equipment import models as equipment
from etcetera.equipment import forms as eqforms
from etcetera.extras.search import get_query

@login_required
def index(request):
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
		equipment_query = get_query(
			query_string, [
				'equipment_type__name',
				'make__name',
				'model',
				'barcode',
				'building__name',
				'room',
				'serial',
				'smsu_id',
				'comments',
			]
		)
		# I'm keeping this longer than 80col because it's a Django filter.
		paged_objects = equipment.Equipment.objects.filter(equipment_query)
	else:
		paged_objects = equipment.Equipment.objects.all()
	
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
		'q': query_string,
	}
	return render_to_response(
		"equipment/index.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def detail(request, object_id):
	# Get the ticket from the URL, bundle it in a context, and send it out.
	wo = get_object_or_404(equipment.Equipment, id=object_id)
	context = {'object': wo,}
	return render_to_response(
		"equipment/detail.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def edit(request, object_id):	
	eq = get_object_or_404(equipment.Equipment, id=object_id)
	if request.method == 'POST':
		form = eqforms.EquipmentModelForm(request.POST, instance=eq)
		if form.is_valid():
			form.save()
			if cd['archived']:
				return HttpResponseRedirect(reverse(
					'equipment-index',
				))
			return HttpResponseRedirect(reverse(
				'equipment-detail',
				args=(eq.id,),
			))
	else:
		form = eqforms.EquipmentModelForm(instance=eq)
	context = {
		'object': eq,
		'form': form,
	}
	return render_to_response(
		"equipment/edit.html",
		context,
		context_instance=RequestContext(request)
	)
