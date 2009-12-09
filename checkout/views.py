import datetime as dt

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from etcetera.checkout import forms as coforms
from etcetera.checkout import models as checkout
from etcetera.checkout.mailer import *
from etcetera.equipment import models as equipment
from etcetera.extras.search import get_query

def checkout_form(request):
	# If data is being sent in POST, then get that data, clean it, and assign
	# it to a new checkout instance.
	if request.method == 'POST':
		form = coforms.CheckoutPublicForm(request.POST)
		if form.is_valid():
			# Form object saves the model in the db itself
			co = form.save()
			# Send an email to the appropriate people using form data
			# created_mail(co)
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
	# Setup our paging and query objects ahead of time
	paged_objects = None
	q = None
	# Set up an empty form
	form = coforms.SearchForm()
	# If there's a GET request, specifically one with a search query
	if request.GET and request.GET.get('q'):
		# Get the data from the search form and put it in a SearchForm object
		form = coforms.SearchForm(request.GET)
		if form.is_valid():
			# If everything's valid, get clean form data and get a list of
			# which boxes were selected
			data = form.cleaned_data
			if data['q'] and data['q'].strip() and form.get_list():
				# This sends a query to search middleware, if such
				# query exists. It gets a Q object back which is used
				# in a Django filter to get our queryset.
				checkout_query = get_query(data['q'], form.get_list())
				paged_objects = checkout.Checkout.objects.filter(
					checkout_query
				)
				q = data['q']
			# If it's not valid or nothing was checked, get all objects from db
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
		'object_list': paged_objects.object_list,
		'form': form,
		'q': q,
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
	# Get the checkout from the URL
	co = get_object_or_404(checkout.Checkout, id=object_id)
	if request.method == 'POST':
		# If POST data is sent, bring in that data to a CheckoutModelForm,
		# validate it, and save it
		form = coforms.CheckoutModelForm(request.POST, instance=co)
		if form.is_valid():
			# If the form isn't previously marked complete, but is now marked
			if not co.completed:
				if form.cleaned_data['completed']:
					# For each associated equipment item
					for eq in co.equipment_list.all():
						# If it's marked as checkedout or overdue
						if eq.status == 'checkedout' or eq.status == 'overdue':
							# Declare a flag that says if it's okay to change
							# an equipment's status
							okay_to_proceed = True
							# For each checkout occuring currently or in the
							# future that the equipment's associated with
							for future_co in eq.checkouts.filter(
								return_date__gte=dt.datetime.now()).filter(
								completed=False):
								# As long as it's not this current checkout
								if future_co != co:
									# Then it's not okay to change the status
									okay_to_proceed = False
							# If okay_to_proceed, then modify the status & save
							if okay_to_proceed:
								eq.status = 'checkout'
								eq.save()
					# completed_mail(co)
			form.save()
			# Then redirect to the detail page for this checkout
			return HttpResponseRedirect(reverse(
				'checkout-detail',
				args=(co.id,),
			))
	# If not post, send a form with prepopulated database info in it
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
		# If there's POST data, fill a CheckoutModelForm object with it
		form = coforms.CheckoutModelForm(request.POST)
		if form.is_valid():
			# If valid, save it into database, which returns the id (to co)
			co = form.save()
			# Also save the user who made it to the ticket
			co.creating_user = request.user
			co.save()
			# created_mail(co)
			# Redirect to the detail page for the new ticket
			return HttpResponseRedirect(reverse(
				'checkout-detail',
				args=(co.id,),
			))
	# If not post, send an empty form to the new template
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
	# Get checkout object from DB
	co = get_object_or_404(checkout.Checkout, id=object_id)
	context = {}
	now = dt.datetime.now()
	if request.method == 'POST':
		# Get form data from POST, fill form object with it
		form = coforms.CheckoutEquipmentForm(request.POST)
		if form.is_valid():
			# Prepare the list of something can't be found (Not Found)
			notfound = {
				'barcodes': [],
				'video_unit': None,
				'cc_unit': None,
			}
			# If there are barcodes, do the following
			if form.cleaned_data['barcodes']:
				# Split the barcodes from the input string
				barcodes = form.cleaned_data['barcodes'].split(" ")
				for item in barcodes:
					try:
						# Get equipment object from DB with that barcode
						eq = equipment.Equipment.objects.get(barcode=item)
						# If the checkout is for the future
						if co.out_date > now:
							# Set the item's status as reserved
							eq.status = 'reserved'
							eq.save()
						if co.out_date < now and co.return_date > now:
							eq.status = 'checkedout'
							eq.save()
						# Check if the equipment is part of a video unit (cart)
						if eq.video_unit:
							# For each equipment in a list of equipment with
							# the same video unit number, add each equipment
							# to the checkout's equipment list
							for vu_item in equipment.Equipment.objects.filter(
								video_unit=eq.video_unit):
								co.equipment_list.add(vu_item)
						else:
							# Otherwise, add the equipment itself
							co.equipment_list.add(eq)
					except equipment.Equipment.DoesNotExist:
						# If the equipment doesn't exist, add the barcode to a
						# list of barcodes to be returned to the user
						notfound['barcodes'].append(item)
			# If there is a video unit, do the following		
			# I'm gonna say this totally violates DRY. May fix sometime soon
			if form.cleaned_data['video_unit']:
				# If the given number even returns any result
				if equipment.Equipment.objects.filter(
					video_unit=form.cleaned_data['video_unit']):
					# Go through each object and add it to co.equipment_list
					for item in equipment.Equipment.objects.filter(
						video_unit=form.cleaned_data['video_unit']):
						# If the checkout is for the future
						if co.out_date > now:
							# Set the item's status as reserved
							item.status = 'reserved'
							item.save()
						if co.out_date < now and co.return_date > now:
							item.status = 'checkedout'
							item.save()
						co.equipment_list.add(item)
				else:
					# Put that in a dictionary to tell the user it wasn't found
					notfound['video_unit'] = form.cleaned_data['video_unit']
			# If there is a computer unit, do the following
			if form.cleaned_data['cc_unit']:
				# If the given number even returns any result
				if equipment.Equipment.objects.filter(
					cc_unit=form.cleaned_data['cc_unit']):
					# Go through each object and add it to co.equipment_list
					for item in equipment.Equipment.objects.filter(
						cc_unit=form.cleaned_data['cc_unit']):
						# If the checkout is for the future
						if co.out_date > dt.datetime.now():
							# Set the item's status as reserved
							item.status = 'reserved'
							item.save()
						if co.out_date < now and co.return_date > now:
							item.status = 'checkedout'
							item.save()
						co.equipment_list.add(item)
				else:
					# Put it in a dictionary to tell the user it wasn't found
					notfound['cc_unit'] = form.cleaned_data['cc_unit']
			# The context to be bundled with the response
			context = {
				'object': co,
				'form': coforms.CheckoutEquipmentForm(),
				'notfound': notfound,
			}
	else:
		# If no POST data coming in, then do up an empty form
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
	# Get the checkout item and the equipment item being sent in the URL
	co = get_object_or_404(checkout.Checkout, id=object_id)
	eq = get_object_or_404(equipment.Equipment, id=eq_id)
	# Request should be GET
	if request.method == 'GET':
		# If the equipment is even in the checkout's equipment list
		if eq in co.equipment_list.all():
			# Remove it, save the checkout
			co.equipment_list.remove(eq)
			co.save()
	# Otherwise, a redirect happens back to the submitting page
	return HttpResponseRedirect(reverse(
		'checkout-equip',
		args=(co.id,),
	))
