from django.conf.urls.defaults import *
from etcetera.mlab.views import *

urlpatterns = patterns('',
	url(r'^$', index, name="mlab-index"),
)