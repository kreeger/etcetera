from django import template

register = template.Library()

@register.inclusion_tag('tags/paginate.html', takes_context=True)
def paginate(context):
	return {
		"paged_objects": context["paged_objects"],
    }