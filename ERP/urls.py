from django.contrib import admin
from django.urls import path, include
from activatedServices.admin import super_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('saijalshakya/', super_admin_site.urls),
    path('', include('system.urls'))
]
