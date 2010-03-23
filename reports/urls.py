from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from etcetera.reports.views import *

urlpatterns = patterns('',
    url(r'^$', index, name="reports-index"),
    url(r'^new/$', new, name="reports-new"),
    url(r'^(?P<slug>.+)/edit/$', edit, name="reports-edit"),
    url(r'^(?P<slug>.+)/(?P<view_type>\w+)/$',
        detail,
        name="reports-detail"
    ),
)