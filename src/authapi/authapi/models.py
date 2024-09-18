from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.validators import RegexValidator


import pyotp, uuid


def default_preferences():
    return {'sms': False, 'email': False, 'app': False}

class UserProfile(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Enter a valid phone number. (e.g., +1234567890 or 1234567890)"
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, max_length=8)
    friends = models.ManyToManyField("UserProfile", blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/", default="images/default_avatar.jpg")

    otp_secret = models.CharField(max_length=32, default=pyotp.random_base32, blank=True)

    tfa = models.JSONField(default=default_preferences)

    sms = models.CharField(max_length=12, blank=True, validators=[phone_regex])
    def __str__(self):
        return self.user.username


class Friend_request(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name="to_user", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["from_user", "to_user"]
