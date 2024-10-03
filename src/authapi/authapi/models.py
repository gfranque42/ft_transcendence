from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.validators import RegexValidator
from django.contrib.sessions.models import Session
    

from django.utils import timezone


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

    jwt = models.TextField(blank=True)

    tfa = models.JSONField(default=default_preferences)


    sms = models.CharField(max_length=13, blank=True, validators=[phone_regex])
    def __str__(self):
        return self.user.username
    def is_logged_in(self):
            # Get all non-expired sessions
        user = self.user
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        
        # Iterate through all sessions
        for session in sessions:
            data = session.get_decoded()  # Decode the session data
            if data.get('_auth_user_id') == str(user.id):  # Compare user ID
                return True
        return False
    
    def games(self):
        # Combine won and lost games, ordered by created_at
        won_games = self.games_won.all()
        lost_games = self.games_loss.all()
        
        # Combine and sort both querysets by created_at
        all_games = list(won_games) + list(lost_games)
        return sorted(all_games, key=lambda game: game.created_at, reverse=True)


class GameHistory(models.Model):
    winner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='games_won')
    loser = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='games_loss')
    score_winner = models.IntegerField(null=True, blank=True)
    score_loser = models.IntegerField(null=True, blank=True)
    game_type = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True) 

class Friend_request(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name="to_user", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["from_user", "to_user"]
