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
    multiplier = models.IntegerField(default=1)

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
    
    def __str__(self):
        return self.dateCompleted


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
    
    # leveling formula, using the current level it determines how much is needed to lvlup
    def calculate_xp_to_lvlup(self, level=None):
        if level == None:
            xp_needed = 5 * (self.level ^ 2) + 500 * self.level + 1000
        else:
            xp_needed = 5 * (level ^ 2) + 500 * level + 1000
        return xp_needed

    # calculates when xp can level up user more than once
    def multiple_lvlup(self, xp):
        running = True
        xp = xp
        level = self.level + 1

        while running:
            if xp >= self.calculate_xp_to_lvlup(level):
                xp -= self.calculate_xp_to_lvlup(level)
                level += 1
            else:
                running = False
        return xp, level

    # handles level logic when xp is sent in a request
    def leveling_up(self, xp):
      # build new object because serializer doesn't accept User objects
        user = model_to_dict(self)
        xp_to_add = xp
        xp_needed = user['xp_to_lvlup']
        new_xp = user['xp'] + xp_to_add
        xp_diff = new_xp - xp_needed

        if xp_diff >= self.calculate_xp_to_lvlup(self.level + 1):
            new_xp, new_level = self.multiple_lvlup(xp_diff)
            user['level'] = new_level
            user['xp'] = new_xp
            user['xp_to_lvlup'] = self.calculate_xp_to_lvlup(new_level)

        elif new_xp >= xp_needed:
            user['level'] += 1
            user['xp'] = xp_diff
            user['xp_to_lvlup'] = self.calculate_xp_to_lvlup(user['level'])

        else:
            user['xp'] = new_xp

        return user

