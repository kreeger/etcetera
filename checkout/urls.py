from django.conf.urls.defaults import *
from etcetera.checkout.views import *

urlpatterns = patterns('',
    url(r'^form/$', checkout_form, name="checkout-form"),
    url(r'^$', index, name="checkout-index"),
    url(r'^new/$', new, name="checkout-new"),
    url(r'^(?P<object_id>\d+)/$', detail, name="checkout-detail"),
    url(r'^(?P<object_id>\d+)/edit/$', edit, name="checkout-edit"),
    url(r'^(?P<object_id>\d+)/equip/$', equip, name="checkout-equip"),
    url(r'^(?P<object_id>\d+)/dupe/$', dupe, name="checkout-dupe"),
    url(r'^(?P<object_id>\d+)/confirm/$', confirm, name="checkout-confirm"),
    url(r'^(?P<object_id>\d+)/activate/$', activate, name="checkout-activate"),
    url(r'^(?P<object_id>\d+)/cancel/$', cancel, name="checkout-cancel"),
    url(r'^(?P<object_id>\d+)/complete/$', complete, name="checkout-complete"),
    url(r'^(?P<object_id>\d+)/equip/rem/(?P<eq_id>\d+)/$',
        equip_remove,
        name="checkout-eqrem"
    ),
    url(r'^(?P<view_type>\w+)/$',
        index,
        name="checkout-index"
    ),
)