from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def redirect_to_main(request):
    return HttpResponseRedirect(reverse('etcetera.views.main'))