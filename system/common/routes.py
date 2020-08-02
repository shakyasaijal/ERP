from django.urls import reverse_lazy
from django.contrib.auth.models import Permission
from system.common import query as query_helper


all_navigation_routes = [
    {
        'title': 'dashboard',
        'url': reverse_lazy('home'),
        'icon': 'fa fa-dashboard',
        'group': False,
        'permission': '',
        'activation': ''
    },
    {
        'title': 'human resource',
        'url': '',
        'icon': 'fa fa-user-secret',
        'group': True,
        'permission': '',
        'activation': 'HRM',
        'links': [
            {
                'title': 'Leave Management',
                'url': '',
                'permission': '',
                'icon': 'fa fa-circle-o'
            },
            {
                'title': 'Attendance',
                'url': '',
                'permission': '',
                'icon': 'fa fa-balance-scale'
            },
            {
                'title': 'Training',
                'url': reverse_lazy('hrm-trainings'),
                'permission': 'hrm.view_training',
                'icon': 'fa fa-book'
            },
            {
                'title': 'Payroll Management',
                'url': reverse_lazy('hrm-trainings'),
                'permission': 'hrm.view_training',
                'icon': 'fa fa-money'
            },
            {
                'title': 'Recruitment',
                'url': reverse_lazy('hrm-trainings'),
                'permission': 'hrm.view_training',
                'icon': 'fa fa-book'
            },
        ]
    },
    {
        'title': 'inventory management',
        'url': '',
        'icon': 'fa fa-archive',
        'group': True,
        'activation': 'IMS',
        'permission': '',
        'links': [
            {
                'title': 'Categories',
                'url': '',
                'permission': '',
                'icon': 'fa fa-circle-o'
            },
            {
                'title': 'Products',
                'url': '',
                'permission': '',
                'icon': 'fa fa-circle-o'
            },
            {
                'title': 'Stocks',
                'url': '',
                'permission': '',
                'icon': 'fa fa-calculator'
            }
        ]
    }
]

def get_routes(user):
    if query_helper.is_branch_manager(user) or user.is_superuser:
        activated_services = query_helper.all_activated_services_for_routes()
        routes = []
        nonTrial = []
        trial = []
        try:
            for route in all_navigation_routes:
                flag = False
                if route['activation']:
                    if route['activation'] in activated_services[0] or route['activation'] in activated_services[1]:
                        flag = True
                else:
                    nonTrial.append(route)

                if flag:
                    if route['activation'] in activated_services[0]:
                        trial.append(route)
                    else:
                        nonTrial.append(route)
        except Exception as e:
            print(e)
            return routes

        routes.append({'system': nonTrial, 'trial': trial})
        return routes
    else:
        return routes_by_permissions(user)


def routes_by_permissions(user):
    users_all_pemissions = Permission.objects.filter(
        group__user=user).order_by('-content_type')
    activated_services = query_helper.all_activated_services_for_routes()
    routes = []
    nonTrial = []
    trial = []
    try:
        for route in all_navigation_routes:
            flag = False
            if route['activation']:
                if route['activation'] in activated_services[0] or route['activation'] in activated_services[1]:
                    if route['permission']:
                        if user.has_perm(data['permission']):
                            flag = True
                    else:
                        flag = True
            else:
                if route['permission']:
                    if user.has_perm(data['permission']):
                        nonTrial.append(route)
                else:
                    nonTrial.append(route)
            if flag:
                if route['activation'] in activated_services[0]:
                    trial.append(route)
                else:
                    nonTrial.append(route)
    except Exception as e:
        print(e)
        return routes

    routes.append({'system': nonTrial, 'trial': trial})
    return routes


def get_formatted_routes(routes, active_page):
    formatted_routes = []
    for route in routes[0].values():
        for r in route:
            r['active'] = False
            if r['title'] == active_page:
                r['active'] = True
        formatted_routes.append(routes)
    return formatted_routes[0]
