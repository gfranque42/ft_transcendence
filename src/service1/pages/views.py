from django.shortcuts import render
from django.http import HttpResponse

def home(request):
<<<<<<< HEAD
<<<<<<< HEAD
    return render(request, 'pages/index.html')
=======
    return render(request, 'pages/base.html')
=======
    return render(request, 'pages/index.html')
>>>>>>> 30b5f14 (🚧 feat: templates with SAP)

def login(request):
    return render(request, 'pages/login.html')

def signup(request):
<<<<<<< HEAD
    return render(request, 'pages/signup.html')
<<<<<<< HEAD
>>>>>>> 9be107d (✨ feat: SAP working)
=======
    return render(request, 'pages/signup.html')
>>>>>>> 7db3f72 (✨ feat: add new app for the pages)
=======
=======
    return render(request, 'pages/signup.html')
>>>>>>> 43a047f (ajusted speeds)
>>>>>>> 7bca8e6 (ajusted speeds)
