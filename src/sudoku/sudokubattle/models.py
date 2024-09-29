from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

""" class SudokuBoard(models.Model):
    row1 = models.CharField(max_length=9, default="---------")
    row2 = models.CharField(max_length=9, default="---------")
    row3 = models.CharField(max_length=9, default="---------")
    row4 = models.CharField(max_length=9, default="---------")
    row5 = models.CharField(max_length=9, default="---------")
    row6 = models.CharField(max_length=9, default="---------")
    row7 = models.CharField(max_length=9, default="---------")
    row8 = models.CharField(max_length=9, default="---------")
    row9 = models.CharField(max_length=9, default="---------")
    start_time = models.DateTimeField(default=timezone.now) # start time of the game

    def __str__(self):
        return f"Sudoku Board ID {self.id}" """

class myUser(models.Model):
	username = models.CharField(max_length=50)
	user_id = models.IntegerField()

class SudokuRoom(models.Model):
    url = models.CharField(max_length=10, unique=True)
    difficulty = models.IntegerField(choices=[(0, 'Easy'), (1, 'Medium'), (2, 'Hard')])
    board = models.JSONField()
    player1 = models.ForeignKey(myUser, related_name='player1', on_delete=models.CASCADE, null=True, blank=True)
    player2 = models.ForeignKey(myUser, related_name='player2', on_delete=models.CASCADE, null=True, blank=True)
    is_full = models.BooleanField(default=False)  # Track if the room is full
    created_at = models.DateTimeField(auto_now_add=True)

    def add_player(self, user):
        """Add a player to the room if there's space."""
        if not self.player1:
            self.player1 = user
        elif not self.player2:
            self.player2 = user
            self.is_full = True  # Mark the room as full once both players are added
        self.save()
