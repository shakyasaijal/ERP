from django.urls import path
from settingsPage import views

urlpatterns = [
    path('', views.GroupsAndPermissions.as_view(), name="groups-and-permissions"),
    path('groups-and-permissions/<int:id>', views.GroupsDetail.as_view(), name="groups-by-id"),
]
