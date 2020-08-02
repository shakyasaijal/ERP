from django.urls import path, include
from system import views

urlpatterns = [
    path('', views.Index.as_view(), name="home"),
    path('login', views.UserLogin.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('forget-password', views.ForgetPassword.as_view(), name="forget-password"),
    path('settings/', include('settingsPage.urls')),
    path('hrm/', include('hrm.urls'))
]
