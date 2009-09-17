from django.conf.urls.defaults import *
from etcetera.equipment.views import *

urlpatterns = patterns('',
	url(r'^$', index, name="equipment-index"),
	url(r'^(?P<object_id>\d+)/$', detail, name="equipment-detail"),
	url(r'^(?P<object_id>\d+)/edit/$', edit, name="equipment-edit"),
	url(r'^new/$', new, name="equipment-new"),
)