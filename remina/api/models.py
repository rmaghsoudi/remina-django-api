from django.db import models

# Create your models here.


class Planet(model.Model):
    description = models.CharField(max_length=140)
    relative = models.IntegerField(default=None)
    # TODO: insert custom validator for the type
    type = models.CharField(max_length=10)
    user = models.IntegerField(default=None)
    xp = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    dateCompleted = models.DateTimeField(auto_now=False, auto_now_add=False)
    dueDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    # TODO: create custom validators for timePeriod and frequency
    timePeriod = models.CharField(max_length=40)
    frequency = models.CharField(max_length=40)
    hId = models.IntegerField(default=None)

# description, relative, type, user, xp, completed
# dateCompleted, dueDate, timePeriod, frequency, hId
