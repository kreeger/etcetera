from django.conf.urls.defaults import *
from etcetera.extras.views import *

urlpatterns = patterns('',
	# url(r'^error_mail/$', error_mail),
	url(r'^change-password/$', change_password, name="change-password"),
)