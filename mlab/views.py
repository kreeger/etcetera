from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def index(request):
	return render_to_response(
		'mlab/index.html',
		{},
		context_instance=RequestContext(request)
	)
