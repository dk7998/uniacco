from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

class User(AbstractUser):
    email       = None
    first_name  = None
    last_name   = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class BankDetails(models.Model):
    account_no = models.IntegerField()
    bank_name  = models.CharField(max_length=150)
    user       = models.ForeignKey(User, related_name='bank_details', on_delete=models.CASCADE)         

    def __str__(self):
        return self.user.username
         

class UserLoginHistory(models.Model):
    user = models.ForeignKey(User, related_name='login_history', on_delete=models.CASCADE)
    ip   = models.GenericIPAddressField()

    def __str__(self):
        return self.user.username

