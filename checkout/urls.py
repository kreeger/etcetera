from django.conf.urls.defaults import *
from etcetera.checkout.views import *

urlpatterns = patterns('',
	url(r'^form/$', checkout_form, name="checkout-form"),
	url(r'^$', index, name="checkout-index"),
	url(r'^completed/$',
		index,
		{'view_type': 'completed'},
		name="checkout-completed"
	),
	url(r'^current/$',
		index,
		{'view_type': 'current'},
		name="checkout-current"
	),
	url(r'^overdue/$',
		index,
		{'view_type': 'overdue'},
		name="checkout-overdue"
	),
	url(r'^deliveries/$',
		index,
		{'view_type': 'deliveries'},
		name="checkout-deliveries"
	),
	url(r'^my_deliveries/$',
		index,
		{'view_type': 'my_deliveries'},
		name="checkout-mine"
	),
	url(r'^new/$', new, name="checkout-new"),
	url(r'^(?P<object_id>\d+)/$', detail, name="checkout-detail"),
	url(r'^(?P<object_id>\d+)/edit/$', edit, name="checkout-edit"),
	url(r'^(?P<object_id>\d+)/equip/$', equip, name="checkout-equip"),
	url(r'^(?P<object_id>\d+)/confirm/$', confirm, name="checkout-confirm"),
	url(r'^(?P<object_id>\d+)/equip/rem/(?P<eq_id>\d+)/$',
		equip_remove,
		name="checkout-eqrem"
	),
)