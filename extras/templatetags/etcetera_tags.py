from django import template
from django.template.defaultfilters import stringfilter

from etcetera.extras import constants

register = template.Library()

@register.inclusion_tag('tags/paginate.html', takes_context=True)
def paginate(context, url_args=''):
	return {
		"paged_objects": context["paged_objects"],
		"url_args": url_args,
    }

# This filter determines how to format a monetary value
# (US currency)
@register.filter
def money(value):
	return "$%.2f" % value

# This filter un-pluralizes
@register.filter
def unpluralize(value, suffix_length=1):
	return value[:-suffix_length]