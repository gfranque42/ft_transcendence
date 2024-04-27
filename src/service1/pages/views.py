from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'pages/base.html')

def login(request):
    return render(request, 'pages/login.html')

def signup(request):
    return render(request, 'pages/signup.html')
