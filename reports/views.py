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
	if view_type not in ['equipmenttypes','departments',]:
		raise Http404
	# Get our report from the Database!
	rp = get_object_or_404(reports.Report.objects.select_related(), slug=slug)
	# Get our checkouts applicable from the database
	cos = checkout.Checkout.objects.select_related().filter(
		canceled=False).filter(
		completion_date__range=(rp.start_date, rp.end_date)
	)
	if view_type == 'departments':
		ou_l = list(rp.organizationalunits.all())
	if view_type == 'equipmenttypes':
		eqt_l = list(rp.equipmenttypes.all())
	ou_d = {}
	eqt_d = {}
	for co in cos:
		if view_type == 'departments':
			if co.department in ou_l:
				incr_item(ou_d, co.department)
		if view_type == 'equipmenttypes':
			for eq in co.equipment_list.all().select_related():
				if eq.equipment_type in eqt_l:
					incr_item(eqt_d, eq.equipment_type)
	context = {
		'object': rp,
		'view_type': view_type,
	}
	if view_type == 'departments':
		context['ou_d'] = sorted(ou_d.iteritems(), key=itemgetter(0))
	if view_type == 'equipmenttypes':
		context['eqt_d'] = sorted(eqt_d.iteritems(), key=itemgetter(0))
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
