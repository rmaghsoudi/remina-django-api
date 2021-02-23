from rest_framework import serializers

from .models import User, Todo, Habit, Goal


class TodoSerializer(serializers.ModelSerializer):
    relatives = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Todo
        fields = ['id', 'description', 'xp',
                  'completed', 'dateCompleted', 'dueDate', 'relatives']


class HabitSerializer(serializers.ModelSerializer):
    relatives = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Habit
        fields = ['id', 'description', 'xp', 'completed',
                  'dateCompleted', 'frequency', 'relatives']


class GoalSerializer(serializers.ModelSerializer):
    relatives = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = ['id', 'description', 'xp', 'completed',
                  'dateCompleted', 'dueDate', 'timePeriod', 'relatives']


class UserSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True)
    habits = HabitSerializer(many=True)
    goals = GoalSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'level', 'username', 'level', 'xp_total',
                  'xp_to_lvlup', 'todos', 'habits', 'goals']
