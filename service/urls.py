from django.conf.urls.defaults import *
from etcetera.service.views import *

urlpatterns = patterns('',
	url(r'^form/$', service_form, name="service-form"),
	url(r'^$', index, name="service-index"),
	url(r'^completed/$', index, {'completed': True}, name="service-completed"),
	url(r'^(?P<object_id>\d+)/$', detail, name="service-detail"),
	url(r'^(?P<object_id>\d+)/edit/$', edit, name="service-edit"),
	url(r'^(?P<object_id>\d+)/pickup/$', pickup, name="service-pickup"),
	url(r'^new/$', new, name="service-new"),
)