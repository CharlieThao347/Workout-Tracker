from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExerciseCategory(models.Model):
    exercises = models.CharField(max_length=128)
    def __str__(self):
        return self.exercises

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.ForeignKey(ExerciseCategory, on_delete=models.CASCADE)

class Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.IntegerField()
