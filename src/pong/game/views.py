from django.shortcuts import render, HttpResponse

def home(request):
	return (render(request, "index.html"))

def index(request):
	return (render(request, "chat.html"))
