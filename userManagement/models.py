from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager)
from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime
import os


def employee_image(instance, filename):
    upload_to = 'employee/static/employee/images/'
    ext = filename.split('.')[-1]
    # get filename
    file_extension = filename.split('.')[1]
    _datetime = datetime.now()
    datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
    date_format = datetime_str.split('-')
    date_join = ''.join(date_format)

    filename = '{}.{}'.format(date_join, ext)
    return os.path.join(upload_to, filename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    address = models.TextField(null=True, blank=True,)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)

    # Custom Fields
    department = models.ManyToManyField(
        'officeStructure.Department', verbose_name="Employee Departments", blank=False)
    date_of_birth = models.DateField(auto_now_add=False, null=True, blank=True)
    branch = models.ManyToManyField('officeStructure.Branches', blank=True)
    phone = models.CharField(max_length=255, null=True,
                             blank=True, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    pan_document = models.FileField(
        verbose_name="PAN Document", upload_to="employee/static/employee/pan/", null=True, blank=True)
    picture = models.ImageField(
        upload_to=employee_image, null=True, blank=True)
    staff_head = models.ForeignKey('self', on_delete=models.PROTECT, related_name="employee_staff_head",
                                   null=True, blank=True, help_text="If Ownership, then not required.")

    designation = models.ForeignKey("officeStructure.Designations", null=True, blank=True, on_delete=models.PROTECT)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        elif self.username:
            full_name = self.username
        else:
            full_name = self.email
        return full_name

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-is_active']


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
