from django.conf.urls.defaults import *
from etcetera.mlab.views import *

urlpatterns = patterns('',
	(r'^$', index),
)