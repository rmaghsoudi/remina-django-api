from django.urls import include, path
from .views import UserView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('users/<int:pk>', UserView.as_view()),
]
