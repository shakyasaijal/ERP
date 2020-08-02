from django.contrib import admin
from . import models


admin.site.register(models.Branches)
admin.site.register(models.Department)
admin.site.register(models.Designations)
admin.site.register(models.Current_Branch)