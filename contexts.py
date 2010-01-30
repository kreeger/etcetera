# Context processors.
from django.conf import settings

from git import *

def template_elements(request):
	# Return a dictionary of values
	return {
		'template_header': 'includes/header.html',
		'template_nav': 'includes/nav.html',
		'template_footer': 'includes/footer.html',
	}

def git_information(request):
	repo = Repo(settings.SITE_ROOT)
	return {
		'current_version': repo.tags[-1].name[1:],
		'current_commit': repo.commits('master', max_count=1)[0].id[:6]
	}

def path_info(request):
	return {
		'path_info': request.META['PATH_INFO'].split('/')[1],
	}

def layout_elements(request):
	return {
		'form_actions': '<ul><li><input type="submit" name="save" value="save" id="save" /></li><li><input type="button" name="go-back" value="go back" id="go-back" /></li></ul>',
	}
