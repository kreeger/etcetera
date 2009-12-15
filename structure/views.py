from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from etcetera.structure import models as structure
from etcetera.structure import forms as stforms
from etcetera.extras.search import get_query

def index(request, structure_kind='buildings'):
	if not structure_kind == 'buildings':
		if not structure_kind == 'departments':
			raise Http404
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
		'type': structure_kind,
		'q': q,
	}
	return render_to_response(
		"structure/index.html",
		context,
		context_instance=RequestContext(request)
	)

def buildings_detail(request, abbreviation):
	bldg = get_object_or_404(
		structure.Building,
		abbreviation=abbreviation
	)
	data = [10, 20, 30]
	context = {'object': bldg,'data': data}
	return render_to_response(
		"structure/buildings_detail.html",
		context,
		context_instance=RequestContext(request)
	)

def organizationalunits_detail(request, object_id):
	ou = get_object_or_404(
		structure.OrganizationalUnit,
		pk=object_id
	)
	context = {'object': ou,}
	return render_to_response(
		"structure/organizationalunits_detail.html",
		context,
		context_instance=RequestContext(request)
	)