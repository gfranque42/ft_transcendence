from django.shortcuts import render
from django.http import HttpResponse

def home(request):
<<<<<<< HEAD
    return render(request, 'pages/index.html')
=======
    return render(request, 'pages/base.html')

def login(request):
    return render(request, 'pages/login.html')

def signup(request):
    return render(request, 'pages/signup.html')
>>>>>>> 9be107d (✨ feat: SAP working)
