from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^login$', views.login, name='login'),  # Endpoint for user login
    re_path(r'^register$', views.RegisterForm.as_view(), name='register'),  # Endpoint for registration
    re_path(r'^test_token$', views.test_token, name='test_token'),  # Endpoint for testing token
]