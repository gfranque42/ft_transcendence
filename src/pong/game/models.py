from django.db import models

# Create your models here.

class TodoItems(models.Model):
	tittle = models.CharField(max_length=200)
	completed = models.BooleanField(default=False)