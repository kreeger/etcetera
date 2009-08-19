from django import template
from etcetera.extras import constants

register = template.Library()

@register.inclusion_tag('tags/paginate.html', takes_context=True)
def paginate(context):
	return {
		"paged_objects": context["paged_objects"],
    }

@register.filter
def priority(priority):
	priority = str(priority)
	branch = {
		'1': 'Urgent',
		'2': 'High',
		'3': 'Medium',
		'4': "Low",
		'5': "Lowest",
	}
	return branch.get(priority, 'No')

@register.filter
def funding_source(funding_source):
	branch = {
		'dept': 'Department',
		'etc': 'ETC',
		'cpu': 'CPU',
		'bc': 'Building Construction',
		'other': 'Other',
		'mgr': 'Mountain Grove',
		'mc': 'Media Collections',
		'scuf': 'SCUF',
	}
	return branch.get(funding_source, 'None')

# This filter determines how to format a monetary value
# (US currency)
@register.filter
def money(value):
	return "$%.2f" % value