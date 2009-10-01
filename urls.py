from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from django.contrib import admin

from etcetera.settings import SITE_ROOT, DEBUG

admin.autodiscover()

# For master/general use.
urlpatterns = patterns('',
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
# etcetera.reports.views

# For university structure management.
# etcetera.structure.views

# For extra things.
urlpatterns += patterns('',
	url(r'^extras/', include('etcetera.extras.urls')),
	url(r'^user/(?P<the_user>.*)/$', 'etcetera.extras.views.profile', name="etcetera-user"),
	url(r'^$', 'etcetera.extras.views.index', name="etcetera-home"),
)