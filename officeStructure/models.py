from django.db import models


class Department(models.Model):
    department_name = models.CharField(
        max_length=255, null=False, blank=False, unique=True, help_text="Customer Service")
    department_head = models.ForeignKey(
        'userManagement.User', on_delete=models.CASCADE, related_name='department_head', null=True, blank=True)

    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name = verbose_name_plural = "All Departments"


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
