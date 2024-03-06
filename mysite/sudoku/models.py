from django.db import models

# Create your models here.

class Sudoku(models.Model):
    puzzle = models.CharField(max_length=81)
    solution = models.CharField(max_length=81)

    def __str__(self):
        return f"Sudoku Puzzle: {self.pk}"