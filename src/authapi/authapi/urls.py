from django.contrib import admin
from django.urls import re_path, path
from authapi.utils import CheckForTFA
from . import views


urlpatterns = [
	path("admin/", admin.site.urls),
    re_path(r'^auth/login$', views.LoginForm.as_view(), name='login'),  # Updated endpoint for user login
    re_path(r'^auth/register$', views.RegisterForm.as_view(), name='register'),  # Endpoint for registration
    re_path(r'^auth/verification$', views.VerifyOTPView.as_view(), name='verification'),  # Endpoint for registration
    re_path(r'^auth/test_token$', views.test_token, name='test_token'),  # Endpoint for testing token
    re_path(r'^auth/profile$', views.Profile.as_view(), name='profile'),  # Endpoint for testing token
]