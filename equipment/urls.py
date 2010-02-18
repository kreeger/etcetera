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
	url(r'^(?P<object_id>\d+)/(?P<history_type>\w+)-history/$',
		history,
		name="equipment-history"
	),
	url(r'^new/$', new, name="equipment-new"),
	url(r'^types/new/$',
		equipmenttype_new,
		name="equipmenttype-new"
	),
	url(r'^types/(?P<slug>.+)/edit/$',
		equipmenttype_edit,
		name="equipmenttype-edit"
	),
	url(r'^types/(?P<slug>.+)/$',
		equipmenttype_detail,
		name="equipmenttype-detail"
	),
	url(r'^types/$',
		equipmenttype_index,
		name="equipmenttype-index"
	),
	url(r'^(?P<view_type>\w+)/$', index, name="equipment-index"),
)