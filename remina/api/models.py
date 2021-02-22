from django.db import models

# Create your models here.


class Goal(models.Model):
    description = models.CharField(max_length=140)
    relative = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    xp = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    dateCompleted = models.DateTimeField(auto_now=False, auto_now_add=False)
    dueDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    # TODO: create custom validator for timePeriod
    timePeriod = models.CharField(max_length=40)


class Habit(models.Model):
    description = models.CharField(max_length=140)
    relative = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    xp = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    dateCompleted = models.DateTimeField(auto_now=False, auto_now_add=False)
    # TODO: create custom validators for frequency
    frequency = models.CharField(max_length=40)


class Todo(models.Model):
    description = models.CharField(max_length=140)
    relative = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    xp = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    dateCompleted = models.DateTimeField(auto_now=False, auto_now_add=False)
    dueDate = models.DateTimeField(auto_now=False, auto_now_add=False)


class User(models.Model):
    username = models.CharField(
        max_length=100,
        unique=True,
    )
    level = models.IntegerField(
        default=1,
    )
    xp_total = models.IntegerField(
        default=0,
    )
    xp_to_lvlup = models.IntegerField(
        default=1515,
    )

# attributes for the user class: an identifier (email, username, etc..), level,
