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
	if value[-2:] == u'es': return value[:-2]
	else: return value[:-suffix_length]

# From http://w.holeso.me/2008/08/a-simple-django-truncate-filter/
@register.filter("truncate_chars")  
def truncate_chars(value, max_length):  
    if len(value) > max_length:  
        truncd_val = value[:max_length]  
        if value[max_length+1] != " ":  
            truncd_val = truncd_val[:truncd_val.rfind(" ")]  
        return truncd_val  
    return value