from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'pages/index.html')

def login(request):
    return render(request, 'pages/login.html')

def signup(request):
<<<<<<< HEAD
    return render(request, 'pages/signup.html')
=======
    return render(request, 'pages/signup.html')
>>>>>>> 43a047f (ajusted speeds)
