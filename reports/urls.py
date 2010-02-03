from django.conf.urls.defaults import *
from etcetera.reports.views import *

urlpatterns = patterns('',
	url(r'^$', index, name="reports-index"),
)