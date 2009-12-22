from django.conf.urls.defaults import *
from etcetera.checkout.views import *

urlpatterns = patterns('',
	url(r'^form/$', checkout_form, name="checkout-form"),
	url(r'^$', index, name="checkout-index"),
	url(r'^completed/$', index, {'completed': True}, name="checkout-completed"),
	url(r'^current/$', index, {'current': True}, name="checkout-current"),
	url(r'^new/$', new, name="checkout-new"),
	url(r'^(?P<object_id>\d+)/$', detail, name="checkout-detail"),
	url(r'^(?P<object_id>\d+)/edit/$', edit, name="checkout-edit"),
	url(r'^(?P<object_id>\d+)/equip/$', equip, name="checkout-equip"),
	url(r'^(?P<object_id>\d+)/equip/rem/(?P<eq_id>\d+)/$',
		equip_remove,
		name="checkout-eqrem"
	),
)