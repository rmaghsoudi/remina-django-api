from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    todos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    habits = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    goals = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'level', 'username', 'level', 'xp_total',
                  'xp_to_lvlup', 'todos', 'habits', 'goals']
