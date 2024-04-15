from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm

# Create your views here.
def register(response):
    if response.method == "POST":
        form = CreateUserForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateUserForm()
    print(form)
    return render(response, "register/register.html", {"form":form})