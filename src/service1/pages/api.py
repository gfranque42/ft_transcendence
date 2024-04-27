
# from .models import Subscribe
from django.http import JsonResponse


def home(request):
  
    # subscribers = Subscribe.objects.values('email', 'date_submitted')
    data = {
        'Home' : True
    }
    return JsonResponse(data)