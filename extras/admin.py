from etcetera.extras.models import Post, UserProfile
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

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
    )
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'title',
    )


# Register the appropriate models 
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)