from django.core.exceptions import PermissionDenied
from userManagement import models as user_models
from system.common import query as query_helper
from functools import wraps


def has_permission(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        # if not request.user.has_perm(perm) and not query_helper.has_all_access(request.user):
        #     return False
        return function(request, *args, **kwargs)
    return _wrapped_view
