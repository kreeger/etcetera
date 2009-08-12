from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from etcetera.service import models as repair
from etcetera.service import forms as woforms
from etcetera.extras.mailer import wo_mail

def service_form(request):
	if request.method == 'POST':
		form = woforms.ServiceForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			wo = repair.WorkOrder()
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
	paginator = Paginator(repair.WorkOrder.objects.filter(archived=archived), 25)
	
	# Make sure page request is of int type -- if not, then deliver page 1
	try:
		page = int(request.GET.get('page','1'))
	except ValueError:
		page = 1
	
	# If page request is out of range, deliver last page of results
	try:
		workorders = paginator.page(page)
	except (EmptyPage, InvalidPage):
		workorders = paginator.page(patinator.num_pages)
	
	context = {
		'workorders': workorders,
		'archived': archived,
	}
	return render_to_response("service/index.html", context, context_instance=RequestContext(request))