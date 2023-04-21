from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False)
    job_title = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @classmethod
    def get_user(cls, query):
        return cls.objects.filter(**query).first()

    def __str__(self):
        return self.email
