from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'username')
    search_fields = ('first_name', 'last_name', 'phone', 'username', 'email', 'address', 'date_of_birth')
    list_filter = ('staff_head',)
    list_per_page = 20
    list_select_related = True


admin.site.register(models.User, UserAdmin)
