from django.conf.urls.defaults import *
from etcetera.checkout.views import *

urlpatterns = patterns('',
	url(r'^$', index, name="checkout-index"),
	url(r'^new/$', new, name="checkout-new"),
	url(r'^(?P<object_id>\d+)/$', detail, name="checkout-detail"),
	url(r'^(?P<object_id>\d+)/edit/$', edit, name="checkout-edit"),
	url(r'^(?P<object_id>\d+)/equip/$', equip, name="checkout-equip"),
)