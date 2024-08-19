from django.db import models
from django.utils import timezone

class SudokuBoard(models.Model):
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
        return f"Sudoku Board ID {self.id}"

class SudokuRoom(models.Model):
    url = models.CharField(max_length=100, unique=True)
    difficulty = models.IntegerField()
    board = models.JSONField()  # To store the Sudoku board as JSON
    created_at = models.DateTimeField(auto_now_add=True)
