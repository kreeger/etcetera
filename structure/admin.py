from etcetera.structure.models import College, Department, SubDepartment, Campus, Building
from django.contrib import admin

# This file determines what's shown in the admin interface

class DepartmentInline(admin.StackedInline):
	model = Department

class SubDepartmentInline(admin.StackedInline):
	model = SubDepartment

class CollegeAdmin(admin.ModelAdmin):
	list_display = ('name','abbreviation',)
	search_fields = ('name','abbreviation',)
	inlines = [DepartmentInline,]

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('name','college',)
	search_fields = ('name','college',)
	inlines = [SubDepartmentInline,]
	list_filter = ('college',)

class SubDepartmentAdmin(admin.ModelAdmin):
	list_display = ('name','department',)
	search_fields = ('name','department',)

class BuildingAdmin(admin.ModelAdmin):
	list_display = ('name','abbreviation',)
	search_fields = ('name','abbreviation',)

# Register the appropriate models 
admin.site.register(College, CollegeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(SubDepartment, SubDepartmentAdmin)
admin.site.register(Campus)
admin.site.register(Building, BuildingAdmin)