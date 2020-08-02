from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.urls import reverse
import yaml

from userManagement import models as user_models
from system.common import query as query_helper
from system.common import system as system_helper
from system.common import routes as navbar

"""
Template
"""
credential = yaml.load(open('credentials.yaml'), Loader=yaml.FullLoader)
template_version = ''
try:
    template_version = credential['template_version']
    template_version = "system/"+template_version
except Exception as e:
    template_version = 'system/v1'


class Index(LoginRequiredMixin, View):  
    def get(self, request):
        routes = navbar.get_formatted_routes(navbar.get_routes(request.user), active_page='dashboard')
        context = {}
        context.update({"routes": routes})
        return render(request, template_version+"/IndexView/index.html", context=context)


class UserLogin(View):
    def get(self, request):
        return render(request, template_version+"/LoginView/login.html", context={'title': 'Login'})

    def post(self, request):
        try:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in.')
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, 'Invalid credentials.')
                return HttpResponseRedirect(reverse('login'))
        except (user_models.User.DoesNotExist, Exception) as e:
            print(e)
            messages.warning(request, 'Something went wrong. Please try again')
            return HttpResponseRedirect(reverse('login'))


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, "You are now logged out.")
        return HttpResponseRedirect(reverse('login'))


class ForgetPassword(View):
    def get(self, request):
        return render(request, template_version+"/Authentication/forgetPassword.html")

    def post(self, request):
        try:
            user = user_models.User.objects.get(email=request.POST['email'])
            email_data = {
                "current_site": get_current_site(request).domain,
                "secure": request.is_secure() and "https" or "http",
                "email": user.email,
                "name": user.first_name
            }
            if send_email.send_email.delay("Password Reset Request", email_data):
                messages.success(
                    request, 'Email has been sent to reset your password.')
                return HttpResponseRedirect(reverse('vendor-login'))
            else:
                messages.warning(
                    request, 'Email was not able to sent. Please try again.')
                return HttpResponseRedirect(reverse('forget-password'))
        except (api_models.User.DoesNotExist, Exception) as e:
            print(e)
            messages.danger(
                request, 'This email is not registered in our system.')
            return HttpResponseRedirect(reverse('forget-password'))

