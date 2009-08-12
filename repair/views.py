from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from etcetera.repair import models as repair
from etcetera.repair import forms as repairforms

def service_form(request):
	if request.method == 'POST':
		form = repairforms.ServiceForm(request.POST)
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
			wo.barcode = cd['barcode']
			wo.description = cd['description']
			wo.save()
			return HttpResponseRedirect('/thanks.html')
	else:
		form = repairforms.ServiceForm()
	context = {'form':form,}
	return render_to_response("repair/service_form.html", context, context_instance=RequestContext(request))