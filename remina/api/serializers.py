from rest_framework import serializers

from .models import User, Todo, Habit, Goal


class TodoSerializer(serializers.ModelSerializer):
    relatives = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Todo
        fields = ['id', 'description', 'xp', 'user',
                  'completed', 'dateCompleted', 'dueDate', 'relatives']


class HabitSerializer(serializers.ModelSerializer):
    relatives = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Habit
        fields = ['id', 'description', 'xp', 'completed', 'user',
                  'dateCompleted', 'frequency', 'relatives']


class GoalSerializer(serializers.ModelSerializer):
    relatives = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = ['id', 'description', 'xp', 'completed', 'user',
                  'dateCompleted', 'dueDate', 'timePeriod', 'relatives']


class UserSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, required=False)
    habits = HabitSerializer(many=True, required=False)
    goals = GoalSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'level', 'username', 'level', 'xp_total',
                  'xp_to_lvlup', 'todos', 'habits', 'goals']
