from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from etcetera.settings import SITE_ROOT, PROD

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# For master/general
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
	(r'^login/$', login),
	(r'^logout/$', logout),
	(r'^profile/$', 'etcetera.views.redirect_to_main'),
	(r'^$', 'etcetera.views.main'),
)

# For serving media content
if PROD == False:
	urlpatterns += patterns('',
		(r'^_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': (SITE_ROOT + '/_media')}),
		(r'^$', 'etcetera.views.redirect_to_main'),
	)

# For equipment management
# etcetera.equipment.views

# For checkout/reservation management
# etcetera.checkout.views

# For repair/service management
# etcetera.repair.views

# For mLab resource management
urlpatterns += patterns('etcetera.mlab.views',
	(r'^mlab/$', 'index'),
)

# For report generation
# etcetera.reports.views

# For university structure management
# etcetera.structure.views