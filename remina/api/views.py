from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import User, Todo, Habit, Goal
from .serializers import UserSerializer, TodoSerializer, HabitSerializer, GoalSerializer

# Create your views here.


class UserView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, format=None):
        new_user = request.data.user
        serializer = UserSerializer(data=new_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO: add leveling functionality to edit how patches work
    # def patch(self, request, pk, format=None):
    #     user = self.get_object(pk)
    #     updated_user = user.leveling_up(int(request.data['xp']))
    #     serializer = UserSerializer(user, data=updated_user)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
