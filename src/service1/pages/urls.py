from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="base-home"),
    path('login/', views.login, name="base-login"),
    path('signup/', views.signup, name="base-signup"),

]