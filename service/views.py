from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from etcetera.service import models as service
from etcetera.service import forms as woforms
from etcetera.extras.mailer import wo_mail
from etcetera.extras.search import get_query

def service_form(request):
	if request.method == 'POST':
		form = woforms.ServiceForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			wo = service.WorkOrder()
			# bind form data to new WorkOrder
			name = cd['name'].split(' ')
			wo.first_name = name[0]
			wo.last_name = name[-1]
			wo.department = cd['department']
			wo.phone = cd['phone']
			wo.email = cd['email']
			wo.building = cd['building']
			wo.room = cd['room']
			wo.equipment_text = cd['equipment_text']
			wo.equipment = wo.barcode_lookup(cd['barcode'])
			wo.description = cd['description']
			wo.work_type = cd['work_type']
			wo.save()
			wo_mail(wo)
			return HttpResponseRedirect('/thanks.html')
	else:
		form = woforms.ServiceForm()
	context = {'form':form,}
	return render_to_response("service/service_form.html", context, context_instance=RequestContext(request))

@login_required
def index(request, archived=False):
	# Warning: the following may not be very Pythonic
	query_string = ''
	paged_objects = None
	if (request.GET):
		if ('q' in request.GET) and request.GET['q'].strip():
			query_string = request.GET['q']
			request.session['q'] = query_string
		else:
			if ('q' in request.session):
				query_string = request.session['q']
	else:
		request.session['q'] = None
		query_string = None
		
	if (query_string):
		service_query = get_query(query_string, ['first_name','last_name','department','equipment__equipment_type__name','equipment__make__name','equipment__model','equipment_text','building__name','room','description',])
		paged_objects = service.WorkOrder.objects.filter(service_query).filter(archived=archived).order_by('-creation_date')
	else:
		paged_objects = service.WorkOrder.objects.filter(archived=archived)
		
	paginator = Paginator(paged_objects, 20)
	# Make sure page request is of int type -- if not, then deliver page 1
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	# If page request is out of range, deliver last page of results
	try:
		paged_objects = paginator.page(page)
	except (EmptyPage, InvalidPage):
		paged_objects = paginator.page(paginator.num_pages)
	
	context = {
		'paged_objects': paged_objects,
		'archived': archived,
		'q': query_string,
	}
	return render_to_response("service/index.html", context, context_instance=RequestContext(request))

def detail(request, object_id):
	ticket = get_object_or_404(service.WorkOrder, id=object_id)
	
	context = {
		'object': ticket,
	}
	return render_to_response("service/detail.html", context, context_instance=RequestContext(request))
