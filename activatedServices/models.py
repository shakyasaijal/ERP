from django.db import models
from helper import choices


class services_requested(models.Model):
    service = models.CharField(max_length=255,
        choices=choices.services, null=False, blank=False, unique=True)
    is_trial = models.BooleanField(choices=choices.yes_no, null=False, blank=False, default=1)
    trail_end = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=False, blank=False)
    started_from = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.service

    class Meta:
        verbose_name = verbose_name_plural = "Services Requested"

    def get_service_name(self):
        return self.service