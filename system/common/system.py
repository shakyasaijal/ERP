from activatedServices import models as service_models


def all_activated_services():
    return service_models.services_requested.objects.all()
    
