from django.shortcuts import render
from django.http import Http404, HttpResponseServerError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from functools import wraps
from .models import User, Todo, Habit, Goal, Check
from .serializers import UserSerializer, TodoSerializer, HabitSerializer, GoalSerializer, CheckSerializer
from .helpers import clear_empty_obj_values, one_week_ago, one_month_ago, to_dict, create_check_array, goal_res_processor, yesterday
import jwt
from functools import wraps
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Create your views here.


def get_token_auth_header(request):
    """Obtains the access token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope

def get_and_level_user(id, xp, multiplier=None, habit_id=None):
    user = User.objects.get(pk=id)
    if multiplier and habit_id:
        updated_user = user.leveling_up(100 * xp)
        habit = Habit.objects.get(pk=habit_id)
        if habit.checks.last().timestamp.date == yesterday():
            habit.multiplier = 1
        else:
            habit.multiplier += 1
        habit.save()
    else:
        updated_user = user.leveling_up(int(xp))
    serializer = UserSerializer(user, data=updated_user)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def calculate_goal_xp(goal):
    xp = 100
    if goal.timePeriod == 'day':
        xp *= 10
    elif goal.timePeriod == 'week':
        xp *= 50
    elif goal.timePeriod == 'month':
        xp *= 100
    return xp

def get_user_from_req(username):
    user = User.objects.get(username=username)
    return user

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
        u, created = User.objects.get_or_create(username=request.data['user']['username'])
        u_serializer = UserSerializer(u)

        if created:
            return Response(u_serializer.data, status=status.HTTP_201_CREATED)
        else:
            u_serializer = UserSerializer(u)
            return Response(u_serializer.data)

        return Response(u_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            user = get_user_from_req(self.request.query_params.get('username'))
            return Todo.objects.filter(user=user.id)   
        except:
            raise HttpResponseServerError

    def get(self, request, format=None):
        todos = self.get_objects()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        new_todo = request.data
        serializer = TodoSerializer(data=new_todo)
        if serializer.is_valid():
            serializer.save()
            if (serializer.data['completed'] == True):
                get_and_level_user(serializer.data['user'], serializer.data['xp'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        updated_todo = clear_empty_obj_values(request.data)
        if 'completed' in updated_todo:
            if (todo.completed == False) and (updated_todo['completed'] == True):
                get_and_level_user(todo.user.id, todo.xp)
        serializer = TodoSerializer(todo, data=updated_todo, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo = self.get_object(pk)
        todo.delete()
        return Response({'message': 'Todo deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class HabitView(APIView):

    def get_objects(self):
        try:
            user = get_user_from_req(self.request.query_params.get('username'))
            habits = Habit.objects.filter(user=user.id)
            current_week_habits = to_dict(habits)
            for i in range(0, len(current_week_habits)):
                checks = habits[i].checks.filter(timestamp__gte=one_week_ago())
                current_week_checks = to_dict(checks)
                complete_check_array = create_check_array(current_week_checks)
                current_week_habits[i]['checks'] = complete_check_array
                current_week_habits[i]['flags'] = {}
                current_week_habits[i]['flags']['todayCompleted'] = False
                if type(current_week_habits[i]['checks'][datetime.today().weekday()]) is dict:
                    current_week_habits[i]['flags']['todayCompleted'] = True

            return current_week_habits
        except:
            raise HttpResponseServerError

    def get(self, request, format=None):
        habits = self.get_objects()
        # serializer = HabitSerializer(habits, many=True)
        return Response(habits)

    def post(self, request, format=None):
        new_habit = request.data
        serializer = HabitSerializer(data=new_habit)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HabitDetailView(APIView):

    def get_object(self, pk):
        try:
            return Habit.objects.get(pk=pk)
        except Habit.DoesNotExist:
            raise Http404

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

    def get_objects(self):
        try:
            user = get_user_from_req(self.request.query_params.get('username'))
            goals = to_dict(Goal.objects.filter(user=user.id, completed=False))
            processed_goals = goal_res_processor(goals)
            return processed_goals
        except:
            raise HttpResponseServerError

    def get(self, request, format=None):
        goals = self.get_objects()
        # serializer = GoalSerializer(goals, many=True)
        return Response(goals)

    def post(self, request, format=None):
        new_goal = request.data
        serializer = GoalSerializer(data=new_goal)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GoalDetailView(APIView):

    def get_object(self, pk):
        try:
            return Goal.objects.get(pk=pk)
        except Goal.DoesNotExist:
            raise Http404


    def patch(self, request, pk, format=None):
        goal = self.get_object(pk)
        serializer = GoalSerializer(goal, data=request.data)
        if (goal.completed == False) and (request.data['completed'] == True):
            get_and_level_user(goal.user.id, calculate_goal_xp(goal))
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
        habit = Habit.objects.get(pk=request.data['habit'])
        new_check = request.data
        serializer = CheckSerializer(data=new_check)
        if serializer.is_valid():
            serializer.save()
            get_and_level_user(habit.user.id, habit.multiplier, True, habit.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
