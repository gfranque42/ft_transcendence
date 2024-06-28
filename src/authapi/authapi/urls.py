from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^auth/login$', views.login, name='login'),  # Updated endpoint for user login
    re_path(r'^auth/register$', views.RegisterForm.as_view(), name='register'),  # Endpoint for registration
    re_path(r'^auth/test_token$', views.test_token, name='test_token'),  # Endpoint for testing token
]