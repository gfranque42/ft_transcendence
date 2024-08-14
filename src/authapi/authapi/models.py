from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.validators import RegexValidator

import pyotp


def default_preferences():
    return {'sms': False, 'email': False, 'app': False}

class UserProfile(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Enter a valid phone number. (e.g., +1234567890 or 1234567890)"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/")

    otp_secret = models.CharField(max_length=32, default=pyotp.random_base32, blank=True)

    tfa = models.JSONField(default=default_preferences)

    sms = models.CharField(max_length=15, blank=True, validators=[phone_regex])
    def __str__(self):
        return self.user.username
