"""
Authentication API URL patterns.

Endpoints:
    - POST /api/registration/ - Register a new user
    - POST /api/login/ - Login user and get authentication token
"""
from django.urls import path

from .views import RegistrationView, LoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login')
]