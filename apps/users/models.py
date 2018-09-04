from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    user
    """
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="name")
    birthday = models.DateField(null=True, blank=True, verbose_name="birthday")
    gender = models.CharField(max_length=6, choices=(("male", "male"), ("female", "female")), default="female",
                              verbose_name="gender")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="mobile")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="email")

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "user"

    def __str__(self):
        return self.name


class VerifyCode(models.Model):
    """
    message verify code
    """
    code = models.CharField(max_length=10, verbose_name="verify code")
    mobile = models.CharField(max_length=11, verbose_name="mobile")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")
    # default time: compile time

    class Meta:
        verbose_name = "message verify code"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
