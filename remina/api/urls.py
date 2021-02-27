from django.urls import include, path
from .views import UserView, TodoView, HabitView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/<int:pk>', UserView.as_view()),
    path('todos/', TodoView.as_view()),
    path('todos/<int:pk>', TodoView.as_view()),
    path('habits/', HabitView.as_view()),
    path('habits/<int:pk>', HabitView.as_view()),
]
