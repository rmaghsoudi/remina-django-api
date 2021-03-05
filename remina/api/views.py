from django.shortcuts import render
from django.http import Http404, HttpResponseServerError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import User, Todo, Habit, Goal, Check
from .serializers import UserSerializer, TodoSerializer, HabitSerializer, GoalSerializer, CheckSerializer

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
        new_user = request.data
        serializer = UserSerializer(data=new_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO: edit how patches work to encompass other patch requests (other than xp reqs)
    def patch(self, request, pk, format=None):
        user = self.get_object(pk)
        updated_user = user.leveling_up(int(request.data['xp']))
        serializer = UserSerializer(user, data=updated_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class TodoView(APIView):

    def get_objects(self):
        try: 
           return Todo.objects.filter(user=self.request.query_params.get('user_id'))   
        except:
            raise HttpResponseServerError

    def get(self, request, format=None):
        todos = self.get_objects()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)


class TodoDetailView(APIView):

    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo = self.get_object(pk)
        todo.delete()
        return Response({'message': 'Todo deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class HabitView(APIView):

    def get_object(self, pk):
        try:
            return Habit.objects.get(pk=pk)
        except Habit.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        habit = self.get_object(pk)
        serializer = HabitSerializer(habit)
        return Response(serializer.data)

    def post(self, request, format=None):
        new_habit = request.data
        serializer = HabitSerializer(data=new_habit)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        habit = self.get_object(pk)
        serializer = HabitSerializer(habit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        habit = self.get_object(pk)
        habit.delete()
        return Response({'message': 'Habit deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class GoalView(APIView):

    def get_object(self, pk):
        try:
            return Goal.objects.get(pk=pk)
        except Goal.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        goal = self.get_object(pk)
        serializer = GoalSerializer(goal)
        return Response(serializer.data)

    def post(self, request, format=None):
        new_goal = request.data
        serializer = GoalSerializer(data=new_goal)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        goal = self.get_object(pk)
        serializer = GoalSerializer(goal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        goal = self.get_object(pk)
        goal.delete()
        return Response({'message': 'Goal deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class CheckView(APIView):

    def post(self, request, format=None):
        new_check = request.data
        serializer = CheckSerializer(data=new_check)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
