
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^auth/login$', views.login, name='login'),  # Updated endpoint for user login
    re_path(r'^auth/register$', views.RegisterForm.as_view(), name='register'),  # Endpoint for registration
    re_path(r'^auth/test_token$', views.test_token, name='test_token'),  # Endpoint for testing token
]
"""
URL configuration for authapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.urls import re_path
from . import views

urlpatterns = [
    re_path('login', views.login),  
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),  
]
