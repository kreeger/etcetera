from django.conf.urls.defaults import *
from etcetera.reports.views import *

urlpatterns = patterns('',
	url(r'^$', index, name="reports-index"),
	url(r'^new/$', new, name="reports-new"),
	url(r'^(?P<slug>.*)/$', detail, name="reports-detail"),
	url(r'^(?P<slug>.*)/edit/$', edit, name="reports-edit"),
)