from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from etcetera.service.views import *

urlpatterns = patterns('',
	(r'^form/$', service_form),
	(r'^$', index),
	(r'^archive/$', index, {'archived': True}),
	(r'^(?P<object_id>\d+)/$', detail),
	(r'^(?P<object_id>\d+)/edit/$', edit),
)