# Context processors.
from django.conf import settings

def template_elements(request):
	
	# Return a dictionary of values
	return {
		'template_header': 'includes/header.html',
		'template_nav': 'includes/nav.html',
		'template_footer': 'includes/footer.html',
	}
