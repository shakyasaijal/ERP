from django.db import models
from ckeditor.fields import RichTextField
from helper import choices
from officeStructure import models as office_models
from userManagement import models as user_models


class Training(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    certification = models.BooleanField(choices=choices.yes_no, null=False, blank=False, default=False, help_text="Does this training have certification?")
    description = RichTextField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True, verbose_name="Start Date")
    completed = models.BooleanField(choices=choices.yes_no, null=True, blank=True, default=False)


    branch = models.ManyToManyField(office_models.Branches, blank=True, related_name="employee_trainings", help_text="Show trainings in which branch/branches?")
    employees = models.ManyToManyField(user_models.User, blank=True, related_name="employee_joined")
    branch_accepted = models.ManyToManyField(office_models.Branches, blank=True, null=True, related_name="branch_accepted", help_text="Which branch has accepted for this training?")
    views = models.BigIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Traning"
        verbose_name_plural = "Tranings"


