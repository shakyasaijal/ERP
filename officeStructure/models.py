from django.db import models
from django.contrib.auth.models import Group


class Designations(models.Model):
    name = models.CharField(max_length=255, null=False,
                            blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "Designations/Post"


class Branches(models.Model):
    branch_name = models.CharField(
        max_length=255, null=False, blank=False, unique=True)
    slug = models.SlugField(null=False, blank=False,
                            unique=False, help_text="IGNORE THIS FIELD.")
    location = models.TextField(null=False, blank=False)
    contact = models.CharField(max_length=255, null=False, blank=False)
    branch_head = models.ForeignKey(
        'userManagement.User', on_delete=models.CASCADE, related_name='branch_head', null=True, blank=True)

    def __str__(self):
        return self.branch_name

    class Meta:
        verbose_name = verbose_name_plural = "Branches"


class Department(models.Model):
    department_name = models.CharField(
        max_length=255, null=False, blank=False, help_text="Customer Service")
    department_head = models.ForeignKey(
        'userManagement.User', on_delete=models.CASCADE, related_name='department_head', null=True, blank=True)
    branch = models.ForeignKey(
        Branches, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name = verbose_name_plural = "All Departments"


class Current_Branch(models.Model):
    user = models.OneToOneField(
        'userManagement.User', on_delete=models.CASCADE, null=False, blank=False)
    branch = models.ForeignKey(
        Branches, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.user.get_full_name()+"-"+self.branch.branch_name


Group.add_to_class('branch', models.ForeignKey(
    Branches, on_delete=models.CASCADE, null=False, blank=False))
Group.add_to_class('description', models.TextField(
    null=True, blank=True, help_text="Help others to understand about this group."))
