from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class myUser(models.Model):
	username = models.CharField(max_length=50, unique=True)
	user_id = models.IntegerField(unique=True)

class SudokuRoom(models.Model):
    url = models.CharField(max_length=10, unique=True)
    difficulty = models.IntegerField(choices=[(0, 'Easy'), (1, 'Medium'), (2, 'Hard')])
    board = models.JSONField()
    player1 = models.ForeignKey(myUser, related_name='player1', on_delete=models.CASCADE, null=True, blank=True)
    player2 = models.ForeignKey(myUser, related_name='player2', on_delete=models.CASCADE, null=True, blank=True)
    is_full = models.BooleanField(default=False)  # Track if the room is full
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    multiplayer = models.BooleanField(default=False)

    def add_player(self, user):
        """Add a player to the room if there's space."""
        if not self.player1:
            self.player1 = user
        elif not self.player2:
            self.player2 = user
            self.is_full = True  # Mark the room as full once both players are added
        self.save()
