import datetime as dt

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from etcetera.checkout import forms as coforms
from etcetera.checkout import models as checkout
from etcetera.equipment import models as equipment

def checkout_form(request):
	# If data is being sent in POST, then get that data, clean it, and assign
	# it to a new WorkOrder instance.
	if request.method == 'POST':
		form = coforms.CheckoutPublicForm(request.POST)
		if form.is_valid():
			form.save()
			co_mail(form)
			return HttpResponseRedirect('/thanks.html')
	# If data is not being sent in POST, our form is an empty one.
	else:
		form = coforms.CheckoutPublicForm()
	# Bundle our form in the context and send it out.
	context = {'form':form,}
	return render_to_response(
		"checkout/checkout_form.html",
		context, context_instance=RequestContext(request)
	)

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

def detail(request, object_id):
	# Get the ticket from the URL, bundle it in a context, and send it out.
	co = get_object_or_404(checkout.Checkout, id=object_id)
	context = {'object': co,}
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
	context = {
		'object': co,
		'form': form,
	}
	return render_to_response(
		"checkout/edit.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def new(request):
	if request.method == 'POST':
		form = coforms.CheckoutModelForm(request.POST)
		if form.is_valid():
			co = form.save()
			co.creating_user = request.user
			co.save()
			return HttpResponseRedirect(reverse(
				'checkout-detail',
				args=(co.id,),
			))
	else:
		form = coforms.CheckoutModelForm()
	context = {
		'form': form,
	}
	return render_to_response(
		"checkout/new.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def equip(request, object_id):
	co = get_object_or_404(checkout.Checkout, id=object_id)
	if request.method == 'POST':
		form = coforms.CheckoutEquipmentForm(request.POST)
		if form.is_valid():
			barcodes = form.cleaned_data['barcodes'].split(" ")
			nf = []
			for item in barcodes:
				try:
					co.equipment_list.add(
						equipment.Equipment.objects.get(barcode=item)
					)
				except equipment.Equipment.DoesNotExist:
					nf.append(item)
			context = {
				'object': co,
				'form': coforms.CheckoutEquipmentForm(),
				'nf': nf,
			}
			return render_to_response(
				"checkout/equip.html",
				context,
				context_instance=RequestContext(request)
			)
	else:
		form = coforms.CheckoutEquipmentForm()
	context = {
		'object': co,
		'form': form,
	}
	return render_to_response(
		"checkout/equip.html",
		context,
		context_instance=RequestContext(request)
	)

@login_required
def equip_remove(request, object_id, eq_id):
	co = get_object_or_404(checkout.Checkout, id=object_id)
	eq = get_object_or_404(equipment.Equipment, id=eq_id)
	if request.method == 'GET':
		if eq in co.equipment_list.all():
			co.equipment_list.remove(eq)
			co.save()
	return HttpResponseRedirect(reverse(
		'checkout-equip',
		args=(co.id,),
	))