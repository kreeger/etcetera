from etcetera.extras.models import Post
from django.contrib import admin

# This file determines what's shown in the admin interface
class PostAdmin(admin.ModelAdmin):
	list_display = (
	    'title',
	    'pub_date',
	    'author',
	)
	list_filter = (
		'pub_date',
	)
	search_fields = (
		'title',
		'content',
	)

# Register the appropriate models 
admin.site.register(Post, PostAdmin)