import datetime as dt

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from etcetera.equipment import models as equipment
from etcetera.equipment import forms as eqforms
from etcetera.extras.search import get_query
from etcetera.extras.constants import EQUIPMENT_STATUSES

@login_required
def index(request, view_type=None):
	if view_type not in ['weekly','counts',None]: raise Http404
	paged_objects = None
	q = None
	count = None
	form = eqforms.SearchForm()
	if request.GET and request.GET.get('q'):
		form = eqforms.SearchForm(request.GET)
		if form.is_valid():
			data = form.cleaned_data
			if data['q'] and data['q'].strip() and form.get_list():
				# This sends a query to search middleware, if such
				# query exists. It gets a Q object back which is used
				# in a Django filter to get our queryset.
				equipment_query = get_query(data['q'], form.get_list())
				paged_objects = equipment.Equipment.objects.filter(
					equipment_query
				)
				q = data['q']
	else:
		paged_objects = equipment.Equipment.objects.all()
	if view_type == 'weekly':
		#import pdb; pdb.set_trace()
		paged_objects.object_list = paged_objects.filter(
			on_weekly_checklist=True
		).order_by(
			'equipment_type__name',
			'video_unit',
			'cc_unit',
			'make__name',
			'model',
			'serial',
		)	
		count = paged_objects.object_list.count()
	if view_type == None:	
		count = paged_objects.count()
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
		'view_type': view_type,
		'q': q,
		'count': count,
	}
	return render_to_response(
		"equipment/index.html",
		context,
		context_instance=RequestContext(request)
	)

def counts(request):
	count_dict = {}	
	for eqt in equipment.EquipmentType.objects.all():
		the_dict = {}
		for stat in ['checkout','checkedout','repair',]:
			the_dict[stat[0]] = eqt.equipment_set.filter(
				status=stat[0]).count()
		count_dict[eqt] = the_dict
	context = {
		'count_dict': count_dict,
		'view_type': 'counts',
	}
	return render_to_response(
		"equipment/counts.html",
		context,
		context_instance=RequestContext(request)
	)

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

@login_required
def new(request):
	if request.method == 'POST':
		form = eqforms.EquipmentModelForm(request.POST)
		if form.is_valid():
			eq = form.save()
			return HttpResponseRedirect(reverse(
				'equipment-detail',
				args=(eq.id,),
			))
	else:
		form = eqforms.EquipmentModelForm()
	context = {
		'form': form,
	}
	return render_to_response(
		"equipment/edit.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def dupe(request, object_id):
	eq = get_object_or_404(equipment.Equipment, id=object_id)
	times = []
	i = 1
	if request.method == 'GET':
		form = eqforms.DupeForm(request.GET)
		if form.is_valid():
			while form.cleaned_data['times'] > len(times):
				times.append(i)
				i = i + 1
	if request.method == 'POST':
		the_set = equipment.Equipment.objects.all()
		while i <= int(request.GET.get('times')):
			new_eq = eq
			new_eq.pk = None
			if not the_set.filter(barcode=request.POST[unicode(i)]):
				new_eq.barcode = request.POST[unicode(i)]
			else:
				new_eq.barcode = '######'
			new_eq.save()
			i = i + 1
		return HttpResponseRedirect(reverse(
			'equipment-index',
		))
	else:
		form = eqforms.DupeForm()
	context = {
		'form': form,
		'object': eq,
		'times': times,
	}
	return render_to_response(
		"equipment/dupe.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def inventory(request, object_id):
	eq = get_object_or_404(equipment.Equipment, id=object_id)
	if request.method == 'GET':
		if eq.last_inventoried != dt.datetime.today():
			eq.last_inventoried = dt.datetime.today()
			eq.save()
	return HttpResponseRedirect(reverse('equipment-detail', args=(eq.id,),))

@login_required
def history(request, object_id, history_type):
	eq = get_object_or_404(equipment.Equipment, id=object_id)
	if history_type not in ['checkout','service']: raise Http404
	if history_type == 'checkout': history = eq.checkouts.all()
	if history_type == 'service': history = eq.workorders.all()
	# Repackage everything into paged_objects using Paginator.
	paginator = Paginator(history, 20)
	# Make sure the page request is an int -- if not, then deliver page 1.
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	# If the page request is out of range, deliver the last page of results.
	try:
		history = paginator.page(page)
	except (EmptyPage, InvalidPage):
		history = paginator.page(paginator.num_pages)
	context = {
		'object': eq,
		'history_type': history_type,
		'paged_objects': history,
		'object_list': history.object_list,
	}
	return render_to_response(
		"equipment/history.html",
		context,
		context_instance=RequestContext(request)
	)