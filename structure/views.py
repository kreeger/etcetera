import datetime as dt

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from etcetera.extras.search import get_query
from etcetera.structure import forms as stforms
from etcetera.structure import models as structure
from etcetera.equipment import graphs as eqgraphs

def count_checkouts(ou):
	checkout_count = ou.checkouts.count()
	for kid in ou.children.all():
		checkout_count += count_checkouts(kid)
	return checkout_count

def count_workorders(ou):
	workorder_count = ou.workorders.count()
	for kid in ou.children.all():
		workorder_count += count_workorders(kid)
	return workorder_count

@login_required
def index(request, structure_kind='buildings'):
	if not structure_kind in ['buildings','departments']: raise Http404
	paged_objects = None
	q = None
	form = stforms.SearchForm()
	if request.GET and request.GET.get('q'):
		form = stforms.SearchForm(request.GET)
		if form.is_valid():
			data = form.cleaned_data
			if data['q'] and data['q'].strip():
				# This sends a query to search middleware, if such
				# query exists. It gets a Q object back which is used
				# in a Django filter to get our queryset.
				structure_query = get_query(
					data['q'],
					form.get_list(structure_kind)
				)
				if structure_kind == 'buildings':
					paged_objects = structure.Building.objects.filter(
						structure_query
					)
				if structure_kind == 'departments':
					paged_objects = structure.OrganizationalUnit.objects.filter(
						structure_query
					)
				q = data['q']
	else:
		if structure_kind == 'buildings':
			paged_objects = structure.Building.objects.all()
		if structure_kind == 'departments':
			paged_objects = structure.OrganizationalUnit.objects.all()
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
		'object_list': paged_objects.object_list,
		'form': form,
		'view_type': structure_kind,
		'q': q,
	}
	return render_to_response(
		"structure/index.html",
		context,
		context_instance=RequestContext(request)
	)

def detail(request, abbreviation=None, object_id=None, room=None):
	# In the future: redo this with annotations.
	view_type = None
	stru_obj = None
	if abbreviation:
		# Get our building and let the context know it's a building
		stru_obj = get_object_or_404(
			structure.Building,
			abbreviation=abbreviation.upper()
		)
		view_type = 'buildings'
		# Building-specific information retrieval
		stru_obj.equipment_installed = stru_obj.equipments.filter(
			status='installed'
		)
	elif object_id:
		# Get our department and let the context know it's a department
		stru_obj = get_object_or_404(
			structure.OrganizationalUnit,
			pk=object_id
		)
		view_type = 'departments'
	if room:
		stru_obj.room_checkouts = stru_obj.checkouts.filter(room=room)
		stru_obj.room_workorders = stru_obj.workorders.filter(room=room)
		stru_obj.checkouts.active = stru_obj.checkouts_open.filter(room=room)
		stru_obj.workorders.active = stru_obj.workorders_open.filter(room=room)
		stru_obj.equipment_installed = stru_obj.equipment_installed.filter(
			room=room
		)
	# Call a custom function that gives us back a graph URL in a string
	
	context = {
		'object': stru_obj,
		'view_type': view_type,
		'room': room,
	}
	return render_to_response(
		"structure/detail.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def edit(request, abbreviation=None, object_id=None):
	view_type = None
	stru_obj = None
	form = None
	return_reverse = None
	if abbreviation:
	# Get our building
		stru_obj = get_object_or_404(
			structure.Building,
			abbreviation=abbreviation.upper()
		)
		form = stforms.BuildingModelForm(instance=stru_obj)
		view_type = 'buildings'
	elif object_id:
		stru_obj = get_object_or_404(
			structure.OrganizationalUnit,
			pk=object_id
		)
		form = stforms.OrganizationalUnitModelForm(instance=stru_obj)
		view_type = 'departments'
	if request.method == 'POST':
		if abbreviation:
			form = stforms.BuildingModelForm(request.POST, instance=stru_obj)
		elif object_id:
			form = stforms.OrganizationalUnitModelForm(
				request.POST, instance=stru_obj
			)
		if form.is_valid():
			stru_obj = form.save()
			if abbreviation:
				return_reverse = reverse(
					'building-detail',
					args=(stru_obj.abbreviation,),
				)
			elif object_id:
				return_reverse = reverse(
					'organizationalunit-detail',
					args=(stru_obj.id,),
				)
			return HttpResponseRedirect(return_reverse)
	context = {
		'object': stru_obj,
		'view_type': view_type,
		'form': form,
	}
	return render_to_response(
		"structure/edit.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def new(request, structure_kind):	
	if structure_kind not in ['buildings','departments']: raise Http404
	form = None
	return_reverse = None
	if structure_kind == 'buildings':
		form = stforms.BuildingModelForm()
	else:
		form = stforms.OrganizationalUnitModelForm()
	if request.method == 'POST':
		if structure_kind == 'buildings':
			form = stforms.BuildingModelForm(request.POST)
		else:
			form = stforms.OrganizationalUnitModelForm(request.POST)
		if form.is_valid():
			stru_obj = form.save()
			if structure_kind == 'buildings':
				return_reverse = reverse(
					'building-detail',
					args=(stru_obj.abbreviation,),
				)
			else:
				return_reverse = reverse(
					'organizationalunit-detail',
					args=(stru_obj.id,),
				)
			return HttpResponseRedirect(return_reverse)
	context = {
		'form': form,
		'view_type': structure_kind,
	}
	return render_to_response(
		"structure/edit.html",
		context,
		context_instance=RequestContext(request)
	)