from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email

import pyotp


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=32, default=pyotp.random_base32, blank=True)

    def __str__(self):
        return self.user.username
