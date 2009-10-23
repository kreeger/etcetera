import datetime as dt

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core import serializers
from django.template import RequestContext

from etcetera.checkout import forms as coforms
from etcetera.checkout import models as checkout
from etcetera.equipment import models as equipment

@login_required
def index(request):
	paged_objects = None
	form = coforms.SearchForm()
	if request.GET and request.GET.get('q'):
		form = coforms.SearchForm(request.GET)
		if form.is_valid():
			data = form.cleaned_data
			if data['q'] and data['q'].strip() and form.get_list():
				# This sends a query to search middleware, if such
				# query exists. It gets a Q object back which is used
				# in a Django filter to get our queryset.
				checkout_query = get_query(data['q'], form.get_list())
				paged_objects = checkout.Checkout.objects.filter(
					checkout_query
				)
			else:
				paged_objects = checkout.Checkout.objects.all()
	else:
		paged_objects = checkout.Checkout.objects.all()
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
		#'q': data['q'],
	}
	return render_to_response(
		"checkout/index.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def detail(request, object_id):
	# Get the ticket from the URL, bundle it in a context, and send it out.
	wo = get_object_or_404(checkout.Checkout, id=object_id)
	context = {'object': wo,}
	return render_to_response(
		"checkout/detail.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def edit(request, object_id):	
	co = get_object_or_404(checkout.Checkout, id=object_id)
	if request.method == 'POST':
		form = coforms.CheckoutModelForm(request.POST, instance=co)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(
				'checkout-detail',
				args=(co.id,),
			))
	else:
		form = coforms.CheckoutModelForm(instance=co)
	eqform = coforms.AddEquipmentForm()
	context = {
		'object': co,
		'form': form,
		'eqform': eqform,
	}
	return render_to_response(
		"checkout/edit.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def add_eq(request, object_id):
	error_msg = u"No POST data sent."
	co = get_object_or_404(checkout.Checkout, id=object_id)
	if request.method == 'POST' and request.is_ajax():
		form = coforms.AddEquipmentForm(request.POST)
		if form.is_valid():
			import pdb; pdb.set_trace()
			cd = form.cleaned_data
			try:
				eq = equipment.Equipment.objects.get(barcode=cd['barcode'])
				co.equipment_list.add(eq)
				co.save()
				JSONSerializer = serializers.get_serializer('json')
				json_serializer = JSONSerializer()
				json_serializer.serialize([eq])
				data = json_serializer.getvalue()
			except equipment.Equipment.DoesNotExist:
				data = u"Equipment with that barcode doesn't exist."
			return HttpResponse(data)
	return HttpResponseServerError(error_msg)

@login_required
def rem_eq(request, object_id, eq_id):
	error_msg = u"No POST data sent."
	co = get_object_or_404(checkout.Checkout, id=object_id)
	eq = get_object_or_404(equipment.Equipment, id=eq_id)
	if eq in co.equipment_list.all():
		co.equipment_list.remove(eq)
		co.save()
	return HttpResponseRedirect(reverse(
		'checkout-edit',
		args=(co.id,),
	))
