from django.urls import path
from system import views

urlpatterns = [
    path('', views.Index.as_view(), name="home"),
    path('login', views.UserLogin.as_view(), name="login"),
]
