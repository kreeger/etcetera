from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from django.contrib import admin

from etcetera.settings import SITE_ROOT, DEBUG

admin.autodiscover()

# For master/general use.
urlpatterns = patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', login, name="etcetera-login"),
	url(r'^logout/$', logout, name="etcetera-logout"),
)

# For only when in development.
if DEBUG:
	urlpatterns += patterns('',
		url(r'^_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': (SITE_ROOT + '/_media')}),
	)

# For equipment management.
urlpatterns += patterns('',
	url(r'^equipment/', include('etcetera.equipment.urls')),
)

# For checkout/reservation management.
urlpatterns += patterns('',
	url(r'^checkout/', include('etcetera.checkout.urls')),
)

# For service management.
urlpatterns += patterns('',
	url(r'^service/', include('etcetera.service.urls')),
)

# For mLab resource management.
urlpatterns += patterns('',
	url(r'^mlab/', include('etcetera.mlab.urls')),
)

# For report generation.
urlpatterns += patterns('',
	url(r'^reports/', include('etcetera.reports.urls')),
)

# For university structure management.
urlpatterns += patterns('',
	url(r'^structure/', include('etcetera.structure.urls')),
)

# For extra things.
urlpatterns += patterns('',
	url(r'^extras/', include('etcetera.extras.urls')),
	url(r'^user/', include('etcetera.extras.urls-profile')),
	url(r'^$', 'etcetera.extras.views.index', name="etcetera-home"),
)