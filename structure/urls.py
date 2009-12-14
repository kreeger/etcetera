from django.conf.urls.defaults import *
from etcetera.structure.views import *

# Universal
urlpatterns = patterns('',
	url(r'^(?P<structure_kind>\w+)/$', index, name="structure-index"),
)

# Buildings
urlpatterns += patterns('',
#	url(r'^buildings/(?P<abbreviation>\w{4})/$',
#		buildings_detail,
#		name="buildings-detail"
#	),
)

# Departments
urlpatterns += patterns('',
#	url(r'^departments/(?P<object_id>\d+)/$',
#		departments_detail,
#		name="departments-detail"
#	),
)