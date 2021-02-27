from django.db import models

# Create your models here.


class Goal(models.Model):
    description = models.CharField(max_length=140)
    relative = models.ForeignKey(
        'self',
        related_name='relatives',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        'User',
        related_name='goals',
        on_delete=models.CASCADE,
        blank=True,
    )
    xp = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    dateCompleted = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    dueDate = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    # TODO: create custom validator for timePeriod
    timePeriod = models.CharField(
        max_length=40,
        blank=True,
        )

    def __str__(self):
        return self.description


class Habit(models.Model):
    description = models.CharField(max_length=140)
    relative = models.ForeignKey(
        'self',
        related_name='relatives',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        'User',
        related_name='habits',
        on_delete=models.CASCADE,
        blank=True,
    )
    xp = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    dateCompleted = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    # TODO: create custom validators for frequency
    frequency = models.CharField(
        max_length=40,
        blank=True,
    )

    def __str__(self):
        return self.description


class Todo(models.Model):
    description = models.CharField(max_length=140)
    relative = models.ForeignKey(
        'self',
        related_name='relatives',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        'User',
        related_name='todos',
        on_delete=models.CASCADE,
        blank=True,
    )
    xp = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    dateCompleted = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    dueDate = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.description


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
