from django.contrib import admin
from .models import Goal, Todo, Habit, User, Check

# Register your models here.

admin.site.register(Goal)
admin.site.register(Todo)
admin.site.register(Habit)
admin.site.register(User)
admin.site.register(Check)
