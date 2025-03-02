from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class ExerciseDetails(models.Model):
    workout = models.ForeignKey(
        'Workout',
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
    )
    reps = models.IntegerField()
    sets = models.IntegerField()
    weight = models.IntegerField()

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_now=True)
    exercises = models.ManyToManyField(
        Exercise,
        through=ExerciseDetails
    )
