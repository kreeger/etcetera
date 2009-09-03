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
	url(r'^profile/$', 'etcetera.views.redirect_to_main', name="etcetera-profile"),
)

# For only when in development.
if DEBUG:
	urlpatterns += patterns('',
		url(r'^_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': (SITE_ROOT + '/_media')}),
	)

# For equipment management.
# etcetera.equipment.views

# For checkout/reservation management.
# etcetera.checkout.views

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
	url(r'^$', 'etcetera.extras.views.index', name="etcetera-home"),
)