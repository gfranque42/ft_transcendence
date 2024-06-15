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
