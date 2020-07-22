from django.contrib import admin
from django.contrib.admin import AdminSite
from . import models


class SuperAdmin(AdminSite):
    site_header = "Saijal Shakya"
    site_title = "Super Admin"
    index_title = "Super Admin - Saijal Shakya"


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('get_service_name', 'expiry_date',
                    'is_trial', 'started_from')
    search_fields = ('get_service_name',)
    list_filter = ('is_trial', 'expiry_date')
    fields = (('service', 'is_trial'), 'trail_end', 'expiry_date', 'started_from')


super_admin_site = SuperAdmin(name='super_admin')
super_admin_site.register(models.services_requested, ServiceAdmin)
