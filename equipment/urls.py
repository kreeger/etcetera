from django.conf.urls.defaults import *
from etcetera.equipment.views import *

urlpatterns = patterns('',
	url(r'^$', index, name="equipment-index"),
	url(r'^(?P<object_id>\d+)/$', detail, name="equipment-detail"),
	url(r'^(?P<object_id>\d+)/edit/$', edit, name="equipment-edit"),
	url(r'^(?P<object_id>\d+)/dupe/$', dupe, name="equipment-dupe"),
	url(r'^(?P<object_id>\d+)/inventory/$',
		inventory,
		name="equipment-inventory"
	),
	url(r'^new/$', new, name="equipment-new"),
	url(r'^weekly/$', weekly_list, name="equipment-weekly"),
)