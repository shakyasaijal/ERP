from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import yaml


"""
Template
"""
credential = yaml.load(open('credentials.yaml'), Loader=yaml.FullLoader)
template_version = ''
try:
    template_version = credential['template_version']
except Exception as e:
    template_version = 'v1'



class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_view+"IndexView/index.html", context={'title': 'Dashboard'})


class UserLogin(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_view+"IndexView/index.html", context={'title': 'Dashboard'})
