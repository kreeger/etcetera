import datetime as dt
from operator import itemgetter

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from etcetera.reports import models as reports
from etcetera.reports import forms as rpforms
from etcetera.checkout import models as checkout
from etcetera.extras.search import get_query

def incr_item(dict, key):
	try:
		item = dict[key]
	except KeyError:
		item = 0
	dict[key] = item + 1

@login_required
def index(request):
	paged_objects = None
	q = None
	form = rpforms.SearchForm()
	if request.GET and request.GET.get('q'):
		form = rpforms.SearchForm(request.GET)
		if form.is_valid():
			data = form.cleaned_data
			if data['q'] and data['q'].strip() and form.get_list():
				# This sends a query to search middleware, if such
				# query exists. It gets a Q object back which is used
				# in a Django filter to get our queryset.
				report_query = get_query(data['q'], form.get_list())
				paged_objects = reports.Report.objects.filter(
					report_query
				)
				q = data['q']
	else:
		paged_objects = reports.Report.objects.all()
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
		'q': q,
	}
	return render_to_response(
		"reports/index.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def detail(request, slug, view_type='equipmenttypes'):
	if view_type not in ['equipmenttypes','departments','buildings',]:
		raise Http404
	# Get our report from the Database!
	rp = get_object_or_404(reports.Report, slug=slug)
	# Get our checkouts applicable from the database
	cos = checkout.Checkout.objects.filter(canceled=False)
	# Set up our dictionaries of doom
	eqtype_d = {}
	ou_d = {}
	ou_eq_d = {}
	bldg_d = {}
	bldg_eq_d = {}
	total_d = {}
	# If various things are specified in the report, those are added to the
	# queryset filters one at a time
	if rp.start_date: cos = cos.filter(completion_date__gte=rp.start_date)
	if rp.end_date: cos = cos.filter(completion_date__lte=rp.end_date)
	# If there are equipmenttypes in the report, initiate that dictionary
	eqt_l = []
	ou_l = []
	bldg_l = []
	if rp.equipmenttypes.count():
		for eqt in rp.equipmenttypes.all():
			eqt_l.append(eqt)
	if rp.organizationalunits.count():
		for ou in rp.organizationalunits.all():
			ou_l.append(ou)
	if rp.buildings.count():
		for bldg in rp.buildings.all():
			bldg_l.append(bldg)
	# The master for loop(s)!
	for co in cos:
		for eq in co.equipment_list.all():
			if eq.equipment_type in eqt_l:
				#eqtype_d[eq.equipment_type] += 1
				incr_item(eqtype_d, eq.equipment_type)
			#if co.department in ou_l:
			#	#ou_eq_d[co.department][eq.equipment_type] += 1
			#	incr_item(ou_eq_d[co.department], eq.equipment_type)
			#if co.building in bldg_l:
			#	#bldg_eq_d[co.building][eq.equipment_type] += 1
			#	incr_item(bldg_eq_d[co.building], eq.equipment_type)
		if co.building in bldg_l:
			#bldg_d[co.building] += 1
			incr_item(bldg_d, co.building)
		if co.department in ou_l:
			#ou_d[co.department] += 1
			incr_item(ou_d, co.department)
	# Sort the dictionary
	dataset = {}
	dataset['equipment_type_counts'] = eqtype_d
	dataset['organizational_unit_counts'] = ou_d
	dataset['organizational_unit_equipment_counts'] = ou_eq_d
	dataset['building_counts'] = bldg_d
	dataset['building_equipment_counts'] = bldg_eq_d
	#for a_dict in dataset:
	#	a_dict = sorted(a_dict.iteritems(), key=itemgetter(0))
	context = {
		'object': rp,
		'dataset': dataset,
		'view_type': view_type,
	}
	return render_to_response(
		"reports/detail.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def edit(request, slug):
	rp = get_object_or_404(reports.Report, slug=slug)
	if request.method == 'POST':
		form = rpforms.ReportModelForm(request.POST, instance=rp)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(
				'reports-detail',
				args=(rp.slug, 'equipmenttypes',),
			))
	else:
		form = rpforms.ReportModelForm(instance=rp)
	context = {
		'object': rp,
		'form': form,
	}
	return render_to_response(
		"reports/edit.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def new(request):
	if request.method == 'POST':
		form = rpforms.ReportModelForm(request.POST)
		if form.is_valid():
			rp = form.save()
			# Assign the user as the created_by person
			rp.created_by = request.user
			rp.save()
			return HttpResponseRedirect(reverse(
				'reports-detail',
				args=(rp.slug, 'equipmenttypes',),
			))
	else:
		form = rpforms.ReportModelForm()
	context = {
		'form': form,
	}
	return render_to_response(
		"reports/edit.html",
		context,
		context_instance=RequestContext(request)
	)
