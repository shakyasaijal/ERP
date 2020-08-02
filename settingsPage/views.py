from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.urls import reverse
import yaml

from userManagement import models as user_models
from system.common import query as query_helper
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


class GroupsAndPermissions(LoginRequiredMixin, View):
    def get(self, request):
        all_groups = Group.objects.filter(
            branch=query_helper.current_user_branch(request))
        context = {}
        context.update({"all_groups": all_groups})
        context.update({"title": "Groups And Permissions"})
        routes = navbar.get_formatted_routes(navbar.get_routes(request.user), active_page='')
        context.update({"routes": routes})

        return render(request, template_version+"/SettingsView/Components/Groups.html", context=context)


class GroupsDetail(LoginRequiredMixin, View):
    def get(self, request, id):
        context = {}
        all_perm = []

        group = Group.objects.get(id=id)
        branch = query_helper.current_user_branch(request)
        if group.branch != branch:
            messages.error(request, "Group not found.")
            return HttpResponseRedirect(reverse('groups-and-permissions'))

        permissions = query_helper.permissions_of_group(group)
        all_permissions = Permission.objects.exclude(
            content_type_id__in=query_helper.excluding_permissions())

        for data in all_permissions:
            if data not in permissions:
                all_perm.append(data)
        routes = navbar.get_formatted_routes(navbar.get_routes(request.user), active_page='')

        context.update({"available_permissions": all_perm})
        context.update({"group": group})
        context.update({"permissions": permissions})
        context.update({"routes": routes})
        
        breadcrumb = [
            {
                "title": "Groups and Permissions",
                "link": reverse('groups-and-permissions')
            },
            {
                "title": group.name.capitalize(),
                "link": ""
            }
        ]
        context.update({"breadcrumb": breadcrumb})

        return render(request, template_version+"/SettingsView/Components/GroupsDetails.html", context=context)

