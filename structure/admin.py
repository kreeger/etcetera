from etcetera.structure.models import OrganizationalUnit, Campus, Building
from django.contrib import admin

# This file determines what's shown in the admin interface

class OrganizationalUnitInline(admin.TabularInline):
    model = OrganizationalUnit

class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = ('name','abbreviation','parent',)
    search_fields = ('name','abbreviation','parent__name',)
    raw_id_fields = ('parent',)
    inlines = [OrganizationalUnitInline,]

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name','abbreviation',)
    search_fields = ('name','abbreviation',)

# Register the appropriate models
admin.site.register(OrganizationalUnit, OrganizationalUnitAdmin)
admin.site.register(Campus)
admin.site.register(Building, BuildingAdmin)