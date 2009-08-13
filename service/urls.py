from django.conf.urls.defaults import *
from etcetera.service.views import *

urlpatterns = patterns('',
	(r'^form/$', service_form),
	(r'^$', index),
	(r'^archive/$', index, {'archived': True}),
#	(r'^(?P<ticket>\d+)/$', detail),
)