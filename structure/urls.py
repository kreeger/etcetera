from django.conf.urls.defaults import *
from etcetera.structure.views import *

# Universal
urlpatterns = patterns('',
	url(r'^(?P<structure_kind>\w+)/$', index, name="structure-index"),
	url(r'^(?P<structure_kind>\w+)/new/$', new, name="structure-new"),
)

# Campuses
urlpatterns += patterns('',
	url(r'^campuses/(?P<slug>\w+)/$',
		detail,
		name="campus-detail"
	),
	url(r'^campuses/(?P<slug>\w+)/edit/$',
		edit,
		name="campus-edit"
	),
)

# Buildings
urlpatterns += patterns('',
	url(r'^buildings/(?P<abbreviation>\w{2,4})/$',
		detail,
		name="building-detail"
	),
	url(r'^buildings/(?P<abbreviation>\w{2,4})/edit/$',
		edit,
		name="building-edit"
	),
	url(r'^buildings/(?P<abbreviation>\w{2,4})/(?P<room>.*)/$',
		detail,
		name="building-detail"
	),
)

# Departments
urlpatterns += patterns('',
	url(r'^departments/(?P<object_id>\d+)/$',
		detail,
		name="organizationalunit-detail"
	),
	url(r'^departments/(?P<object_id>\d+)/edit/$',
		edit,
		name="organizationalunit-edit"
	),
)