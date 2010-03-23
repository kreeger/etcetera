from django.conf.urls.defaults import *
from etcetera.extras.views import *

urlpatterns = patterns('',
    url(r'^edit/$', edit_profile, name="user-edit"),
    url(r'^(?P<the_user>.*)/(?P<view_type>.*)/$', profile_related, name="user-related"),
    url(r'^(?P<the_user>.*)/$', profile, name="user-detail"),
)