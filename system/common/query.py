from officeStructure import models as office_models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from activatedServices import models as services_model
from datetime import datetime


def excluding_permissions():
    excludable_models_for_permissions = []
    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='LogEntry'))
    except Exception as e:
        pass

    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='session'))
    except Exception as e:
        pass

    return excludable_models_for_permissions


def permissions_of_group(group):
    excludable_models_for_permissions = excluding_permissions()
    permissions = group.permissions.exclude(
        content_type_id__in=excludable_models_for_permissions).order_by('id')
    return permissions


def permission_of_current_user(user):
    permissions = []
    for data in Permission.objects.filter(group__user=user).order_by('-content_type'):
        permissions.append(data.codename)
    return permissions


def current_user_branch(request):
    current_branch = office_models.Current_Branch.objects.get(
        user=request.user)
    return current_branch.branch


def is_branch_manager(user):
    if office_models.Branches.objects.filter(branch_head=user):
        return True
    return False


def has_all_access(user):
    if office_models.Branches.objects.filter(branch_head=user) or user.is_superuser:
        return True
    return False


def all_activated_services_for_routes():
    data = services_model.services_requested.objects.all()
    trial = []
    nonTrial = []

    for d in data:
        if d:
            if d.is_trial:
                # Trial=Yes
                date_difference = d.trail_end - datetime.now().date()
                if date_difference.days >= 0:
                    trial.append(d.service)
            else:
                # Trial = No
                date_difference = d.expiry_date - datetime.now().date()
                if date_difference.days >= 0:
                    nonTrial.append(d.service)
    return trial, nonTrial
