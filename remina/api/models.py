from django.db import models

# Create your models here.


class Goal(models.Model):
    description = models.CharField(max_length=140)
    user = models.ForeignKey(
        'User',
        related_name='goals',
        on_delete=models.CASCADE,
        blank=True,
    )
    xp = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    # TODO: create custom validator for timePeriod
    timePeriod = models.CharField(
        max_length=40,
        blank=True,
    )

    def __str__(self):
        return self.description


class Habit(models.Model):
    description = models.CharField(max_length=140)
    user = models.ForeignKey(
        'User',
        related_name='habits',
        on_delete=models.CASCADE,
        blank=True,
    )
    xp = models.IntegerField(default=1)

    def __str__(self):
        return self.description


class Todo(models.Model):
    description = models.CharField(max_length=140)
    user = models.ForeignKey(
        'User',
        related_name='todos',
        on_delete=models.CASCADE,
        blank=True,
    )
    xp = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    dueDate = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.description


class Check(models.Model):
    habit = models.ForeignKey(
        'Habit',
        related_name='checks',
        on_delete=models.CASCADE,
        blank=True,
    )
    dateCompleted = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )


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

    def __str__(self):
        return self.username

# attributes for the user class: an identifier (email, username, etc..), level,
