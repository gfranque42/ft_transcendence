from django.shortcuts import render
<<<<<<< HEAD
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm

# Create your views here.
class RegisterForm(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register.html'

    def get(self, request):
        form = CreateUserForm()
        return Response({'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # You might want to redirect or send a success message
            return Response({'form': form, 'success': True})
        return Response({'form': form})
=======

# Create your views here.
>>>>>>> d7d4b2f (🚧 struct: add the structure for the registration)
