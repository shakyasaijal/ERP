from pprint import pprint
from officeStructure import models as office_models
from system.common import query as query_helper


def context_processor(request):
    context = {}
    try:
        user_permissions = query_helper.permission_of_current_user(request.user)
        is_branch_manager = False
        if query_helper.is_branch_manager(request.user):
            is_branch_manager = True

        has_all_access = False
        if request.user.is_superuser or is_branch_manager:
            has_all_access = True

        current_branch = query_helper.current_user_branch(request)
        context.update({"user_permissions": user_permissions})
        context.update({"is_branch_manager": is_branch_manager})
        context.update({"current_branch": current_branch})
        context.update({"has_all_access": has_all_access})
    except Exception as e:
        print("Context Processor: ", e)

    return context
