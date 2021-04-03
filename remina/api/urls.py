from django.urls import include, path
from .views import UserView, TodoView, TodoDetailView, HabitView, HabitDetailView, GoalView, CheckView


urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/<int:pk>', UserView.as_view()),
    path('todos', TodoView.as_view()),
    path('todos/<int:pk>', TodoDetailView.as_view()),
    path('habits', HabitView.as_view()),
    path('habits/<int:pk>', HabitDetailView.as_view()),
    path('goals/', GoalView.as_view()),
    path('goals/<int:pk>', GoalView.as_view()),
    path('checks', CheckView.as_view()),
]
