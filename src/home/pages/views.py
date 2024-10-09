from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'pages/index.html')

# def custom_404_view(request, exception):
#     return render(request, '404.html', status=404)