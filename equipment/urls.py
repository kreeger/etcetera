from django.conf.urls.defaults import *
from etcetera.equipment.views import *

urlpatterns = patterns('',
	url(r'^$', index, name="equipment-index"),
	url(r'^(?P<object_id>\d+)/$', detail, name="equipment-detail"),
	#url(r'^new/$', new, name="equipment-new"),
	#url(r'^form/$', service_form, name="service-form"),
	#url(r'^archive/$', index, {'archived': True}, name="service-archive"),
	#url(r'^(?P<object_id>\d+)/edit/$', edit, name="service-edit"),
	#url(r'^(?P<object_id>\d+)/pickup/$', pickup, name="service-pickup"),
)